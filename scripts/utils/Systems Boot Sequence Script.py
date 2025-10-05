import argparse
import subprocess
import os
import sys
import time
import logging
import toml
import requests
from typing import Dict, Any, List

# --- Constants ---
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "boot_sequence_config.toml")
HEALTH_CHECK_TIMEOUT = 120  # 2 minutes for all services to come up
HEALTH_CHECK_INTERVAL = 5   # 5 seconds between checks

# --- Logger Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

def run_command(command: str, cwd: str = None) -> (bool, str):
    """Executes a shell command and returns success status and output."""
    logging.info(f"Executing: {' '.join(command)}")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            shell=False # Safer
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            logging.info(f"Successfully executed: {' '.join(command)}")
            return True, stdout
        else:
            logging.error(f"Error executing command: {' '.join(command)}")
            logging.error(f"Stderr: {stderr}")
            return False, stderr
    except FileNotFoundError:
        logging.error(f"Command not found: {command[0]}")
        return False, f"Command not found: {command[0]}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False, str(e)


class BootSequenceManager:
    """Manages the startup, reset, and validation of the ApexSigma ecosystem."""

    def __init__(self, config_path: str, args: argparse.Namespace):
        self.args = args
        self.config = self._load_config(config_path)
        self.project_root = os.path.dirname(os.path.dirname(config_path)) # Assumes script is in devenviro.as/scripts
        self.compose_file = os.path.join(self.project_root, self.config['docker']['compose_file'])

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the TOML configuration file."""
        try:
            return toml.load(config_path)
        except FileNotFoundError:
            logging.error(f"Configuration file not found at {config_path}")
            sys.exit(1)
        except toml.TomlDecodeError as e:
            logging.error(f"Error decoding TOML configuration file: {e}")
            sys.exit(1)

    def run(self):
        """Orchestrates the entire boot sequence based on user arguments."""
        logging.info("--- Operation Heimdall: Initiating Systems Boot Sequence ---")

        if self.args.reset:
            self.reset_environment()

        if self.args.purge_context:
            self.purge_context()

        if not self.args.skip_audit:
             if not self.pre_boot_audit():
                 logging.error("Pre-boot audit failed. Aborting startup.")
                 return

        self.start_services()
        self.validate_services()

        logging.info("--- Systems Boot Sequence Completed ---")


    def pre_boot_audit(self) -> bool:
        """Conducts a pre-boot audit of the system."""
        logging.info("--- Phase 0: Conducting Pre-Boot System Audit ---")
        # Check for Docker and Docker Compose
        success, _ = run_command(["docker", "--version"])
        if not success:
            logging.error("Docker is not installed or not in PATH.")
            return False
        success, _ = run_command(["docker-compose", "--version"])
        if not success:
             success, _ = run_command(["docker", "compose", "--version"])
             if not success:
                logging.error("Docker Compose is not installed or not in PATH.")
                return False

        if not os.path.exists(self.compose_file):
            logging.error(f"Standardized compose file not found: {self.compose_file}")
            return False

        logging.info("Pre-boot audit passed.")
        return True


    def reset_environment(self):
        """Stops and removes all containers, and prunes Docker resources."""
        logging.info("--- Resetting Docker Environment ---")
        run_command(["docker-compose", "-f", self.compose_file, "down", "--volumes"], cwd=self.project_root)
        run_command(["docker", "system", "prune", "-af"], cwd=self.project_root)
        logging.info("Environment reset.")


    def purge_context(self):
        """Purges all persistent data from databases and caches (destructive)."""
        logging.warning("--- Purging All Persistent Context (Destructive Operation!) ---")
        # This is a placeholder for a more robust DB/Cache clearing mechanism
        # For now, we rely on the `docker-compose down --volumes` in reset.
        logging.info("Context purge relies on environment reset. Ensure --reset is used.")


    def start_services(self):
        """Starts all services defined in the standardized Docker Compose file."""
        logging.info("--- Starting All Ecosystem Services ---")
        success, _ = run_command(
            ["docker-compose", "-f", self.compose_file, "up", "--build", "-d"],
            cwd=self.project_root
        )
        if not success:
            logging.error("Failed to start services with Docker Compose. Please check logs.")
            sys.exit(1)


    def validate_services(self):
        """Validates that all services are healthy by polling their health endpoints."""
        logging.info("--- Validating Service Health ---")
        start_time = time.time()
        all_healthy = False
        services_to_check = [s for s in self.config['services'] if s.get('health_endpoint')]

        while time.time() - start_time < HEALTH_CHECK_TIMEOUT:
            healthy_count = 0
            for service in services_to_check:
                url = f"http://localhost:{service['port']}{service['health_endpoint']}"
                try:
                    response = requests.get(url, timeout=2)
                    if response.status_code == 200:
                        logging.info(f"✅ Service '{service['name']}' is HEALTHY.")
                        healthy_count += 1
                    else:
                        logging.warning(f"⏳ Service '{service['name']}' is UP but not healthy (Status: {response.status_code}).")
                except requests.ConnectionError:
                    logging.warning(f"⏳ Service '{service['name']}' is not yet reachable.")

            if healthy_count == len(services_to_check):
                all_healthy = True
                break

            logging.info(f"Waiting for services to become healthy ({healthy_count}/{len(services_to_check)})...")
            time.sleep(HEALTH_CHECK_INTERVAL)

        if all_healthy:
            logging.info("🎉 All services are healthy and operational.")
        else:
            logging.error("❌ Timeout reached. Not all services became healthy.")


def main():
    """Main function to parse arguments and run the boot sequence."""
    parser = argparse.ArgumentParser(description="ApexSigma Ecosystem Boot Sequence Manager")
    parser.add_argument("--reset", action="store_true", help="Stop, remove, and prune the entire Docker environment before starting.")
    parser.add_argument("--purge-context", action="store_true", help="Purge all persistent data. Highly destructive. Implies --reset.")
    parser.add_argument("--skip-audit", action="store_true", help="Skip the pre-boot audit phase.")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help=f"Path to the configuration file (default: {DEFAULT_CONFIG_PATH})")

    args = parser.parse_args()

    if args.purge_context:
        args.reset = True # Purging requires a full reset

    manager = BootSequenceManager(config_path=args.config, args=args)
    manager.run()

if __name__ == "__main__":
    main()
