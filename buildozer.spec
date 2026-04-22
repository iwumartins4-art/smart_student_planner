[app]

# (str) Title of your application
title = Smart Student Planner

# (str) Package name
package.name = smart_student_planner

# (str) Package domain (needed for android/ios packaging)
package.domain = com.supsavetech

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,db

# (str) Application versioning (method 1)
version = 2.0.0

requirements = python3, kivy==2.3.1, https://github.com/kivymd/KivyMD/archive/master.zip, pillow, materialyoucolor, requests, android

# (str) Custom source folders for requirements
# packagers often need orientation restricted for student apps
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) indicates if the application should be fullscreen or not
fullscreen = 0

# (bool) Automatically accept Android SDK licenses
android.accept_sdk_license = True

# (list) The Android libs to copy in the project
# android.add_libs_armeabi_v7a = libs/android-v7a/*.so

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
