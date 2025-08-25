#!/bin/bash

# --- Configuration ---
source_dir_relative="AndroidStudioProjects/openapi_pyGlobalSpec/tiktok-business-api-sdk"
target_dir_relative="AndroidStudioProjects/openapi_pyGlobalSpec/openapi-python-sdk"

# --- Get absolute paths from HOME ---
# This makes the script more robust, assuming these are relative to your home directory
source_dir="$HOME/$source_dir_relative"
target_dir="$HOME/$target_dir_relative"

# --- Safety Checks ---
# 1. Ensure source directory exists and is a directory
if [ ! -d "$source_dir" ]; then
  echo "Error: Source directory '$source_dir' not found or is not a directory."
  exit 1
fi

# 2. Ensure target directory exists and is a directory
if [ ! -d "$target_dir" ]; then
  echo "Error: Target directory '$target_dir' not found or is not a directory."
  # You could choose to create it if it doesn't exist:
  # echo "Target directory '$target_dir' not found. Creating it..."
  # mkdir -p "$target_dir"
  # if [ $? -ne 0 ]; then
  #   echo "Error: Could not create target directory '$target_dir'."
  #   exit 1
  # fi
  exit 1 # Current behavior: exit if target doesn't exist
fi

# 3. Ensure source and target are not the same
# realpath resolves symbolic links and '..' to get the canonical path
if [ "$(realpath "$source_dir")" == "$(realpath "$target_dir")" ]; then
  echo "Error: Source and target directories are the same. Aborting."
  exit 1
fi

echo "--- Starting Merge Process ---"
echo "Source: '$source_dir'"
echo "Target: '$target_dir'"
echo "Mode: Merge without overwriting existing files in target."
echo ""

# --- Enable dotglob to make '*' match hidden files ---
# This ensures that files like .gitignore, .htaccess, etc., are also moved.
shopt -s dotglob

# --- Check if source directory has any content ---
# ls -A lists all entries except . and ..
# The output of ls -A is checked. If it's non-empty, the directory has content.
if [ -n "$(ls -A "$source_dir")" ]; then
    echo "Moving contents from '$source_dir' to '$target_dir'..."
    echo "Files in '$target_dir' with the same name will NOT be overwritten."

    # Move all contents (including hidden ones, thanks to dotglob)
    # -v : verbose (shows what is being moved or skipped)
    # -n : no-clobber (do not overwrite an existing file)
    # The trailing slash on "$source_dir"/* is not strictly necessary with dotglob
    # but "$target_dir"/ ensures target is treated as a directory.
    mv -vn "$source_dir"/* "$target_dir"/

    if [ $? -ne 0 ]; then
        # This exit code from mv doesn't necessarily mean failure if -n was used.
        # It might mean some files were not moved because they already existed in the target.
        # The verbose output (-v) from mv will show which files were skipped.
        echo "Note: 'mv' command finished. Review output above to see which files were moved or skipped."
    else
        echo "All items from source (that didn't conflict) moved successfully."
    fi
else
    echo "Source directory '$source_dir' is empty. Nothing to move."
fi

# --- Disable dotglob (good practice to revert shell options) ---
shopt -u dotglob

echo ""
echo "--- Post-Move Cleanup ---"

# --- Remove the source directory IF IT IS EMPTY ---
# This is a crucial safety check. rmdir will fail if the directory is not empty.
if [ -z "$(ls -A "$source_dir")" ]; then # Check if source_dir is now empty
    echo "Source directory '$source_dir' is now empty. Attempting to remove it..."
    rmdir "$source_dir"
    if [ $? -eq 0 ]; then
        echo "Successfully removed empty source directory: '$source_dir'."
    else
        echo "Error: Could not remove source directory '$source_dir' with rmdir."
        echo "This can happen due to permissions or if it somehow still contains special files not listed by 'ls -A'."
    fi
else
    echo "Warning: Source directory '$source_dir' is NOT empty."
    echo "This means some files were NOT moved, likely because they already exist in '$target_dir' and you chose not to overwrite."
    echo "Source directory '$source_dir' will NOT be automatically removed."
    echo "Please review its contents manually: ls -Al '$source_dir'"
fi

echo ""
echo "--- Merge Process Complete ---"
