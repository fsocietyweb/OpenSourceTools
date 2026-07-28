cmake_minimum_required(VERSION 3.16)
project(KWeb LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Sucht nach den benötigten Qt6-Paketen für die UI und die Chromium-Engine
find_package(Qt6 REQUIRED COMPONENTS Widgets WebEngineWidgets)

# Automatische Qt-Tools aktivieren (wichtig für das Q_OBJECT Makro am Ende der Datei)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Definiert den Namen unseres Programms (KWeb) und die Quellcodedatei
add_executable(KWeb main.cpp)

# Verknüpft die Qt6-Bibliotheken mit unserem KWeb-Programm
target_link_libraries(KWeb PRIVATE Qt6::Widgets Qt6::WebEngineWidgets)
