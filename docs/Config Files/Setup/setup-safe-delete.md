# Setup Safe-Delete for Bash/Zsh

This document provides instructions on how to set up the safe-delete function, which overrides the standard `rm` command to prevent accidental permanent deletion of files.

## 1. Locate your shell configuration file

-   For Bash, this is typically `~/.bashrc`.
-   For Zsh, this is typically `~/.zshrc`.

## 2. Add the following lines to your configuration file

Open your `.bashrc` or `.zshrc` file in a text editor and add the following lines to the end of the file. Make sure to replace `/path/to/your/project` with the absolute path to the `ApexSigmaProjects.Dev` directory.

```bash
# ApexSigma Safe-Delete
export APEXSIGMA_PROJECT_ROOT="/path/to/your/project"
if [ -f "$APEXSIGMA_PROJECT_ROOT/scripts/utils/safe-delete.sh" ]; then
    source "$APEXSIGMA_PROJECT_ROOT/scripts/utils/safe-delete.sh"
    alias rm='safe_rm'
fi
```

## 3. Reload your shell configuration

For the changes to take effect, you need to reload your shell configuration. You can do this by running one of the following commands in your terminal:

-   For Bash:

    ```bash
    source ~/.bashrc
    ```

-   For Zsh:

    ```bash
    source ~/.zshrc
    ```

## 4. Verify the setup

To verify that the safe-delete function is working correctly, you can create a test file and then try to remove it.

```bash
# Create a test file
touch test_file.txt

# Try to remove it
rm test_file.txt
```

You should see a message indicating that the file has been moved to the trash directory. You can also check the contents of the `_archive/trash` directory to confirm that the file is there.
