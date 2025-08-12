if(CPACK_PACKAGE_FILE_NAME MATCHES ".*-src$")
    message(FATAL_ERROR "Creating source archives for SDL 3.2.12 is not supported.")
endif()

set(PROJECT_SOURCE_DIR "/home/ethanboi/Desktop/Git/Ethanboilol/Relight-Engine/ThirdParty/SDL3/Src")
set(SDL_CMAKE_PLATFORM "Linux")
set(SDL_CPU_NAMES "")
list(SORT SDL_CPU_NAMES)

string(REPLACE ";" "-" SDL_CPU_NAMES_WITH_DASHES "${SDL_CPU_NAMES}")
if(SDL_CPU_NAMES_WITH_DASHES)
    set(SDL_CPU_NAMES_WITH_DASHES "-${SDL_CPU_NAMES_WITH_DASHES}")
endif()

string(TOLOWER "${SDL_CMAKE_PLATFORM}" lower_sdl_cmake_platform)
string(TOLOWER "${SDL_CPU_NAMES}" lower_sdl_cpu_names)
if(lower_sdl_cmake_platform STREQUAL lower_sdl_cpu_names)
    set(SDL_CPU_NAMES_WITH_DASHES)
endif()

set(MSVC )
set(MINGW )
if(MSVC)
    set(SDL_CMAKE_PLATFORM "${SDL_CMAKE_PLATFORM}-VC")
elseif(MINGW)
    set(SDL_CMAKE_PLATFORM "${SDL_CMAKE_PLATFORM}-mingw")
endif()


set(CPACK_PACKAGE_FILE_NAME "SDL3-3.2.12-${SDL_CMAKE_PLATFORM}${SDL_CPU_NAMES_WITH_DASHES}")

if(CPACK_GENERATOR STREQUAL "DragNDrop")
    set(CPACK_DMG_VOLUME_NAME "SDL3 3.2.12")
    # FIXME: use pre-built/create .DS_Store through AppleScript (CPACK_DMG_DS_STORE/CPACK_DMG_DS_STORE_SETUP_SCRIPT)
    set(CPACK_DMG_DS_STORE "${PROJECT_SOURCE_DIR}/Xcode/SDL/pkg-support/resources/SDL_DS_Store")
endif()
