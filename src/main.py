import os
import shutil


def copy_static(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    _copy_recursive(src, dest)


def _copy_recursive(src, dest):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} → {dest_path}")
            shutil.copy(src_path, dest_path)

        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_recursive(src_path, dest_path)


def main():
    copy_static("static", "public")


if __name__ == "__main__":
    main()
