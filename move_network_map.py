import os
import shutil

# Create archive directory
archive_dir = r"C:\Users\steyn\ApexSigmaProjects.Dev\docs\Config Files\Infrastructure\Docker Network\_archive"
os.makedirs(archive_dir, exist_ok=True)
print("Archive directory created or already exists")

# Move the old network map to the archive directory
old_map = r"C:\Users\steyn\ApexSigmaProjects.Dev\docs\Config Files\Infrastructure\Docker Network\VERIFIED_DOCKER_NETWORK_MAP.md"
new_location = r"C:\Users\steyn\ApexSigmaProjects.Dev\docs\Config Files\Infrastructure\Docker Network\_archive\VERIFIED_DOCKER_NETWORK_MAP.md"

if os.path.exists(old_map):
    shutil.move(old_map, new_location)
    print("Old network map moved to archive directory")
else:
    print("Old network map not found")
