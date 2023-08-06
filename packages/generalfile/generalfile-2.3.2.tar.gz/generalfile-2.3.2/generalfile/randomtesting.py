


from generalfile import Path
# from generalfile.test.setup_workdir import setup_workdir
# setup_workdir()
# Path.get_working_dir().open_folder()
# Path.get_lock_dir().open_folder()



path = Path().absolute()

path = path.get_parent(-1)

print(path)


# list(path.get_paths_recursive())

# path.get_parent(-1).view()
