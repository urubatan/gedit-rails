#!/bin/sh

killall gedit
sudo cp rails.xml /usr/share/mime/packages
sudo update-mime-database /usr/share/mime
sudo cp erb.lang /usr/share/gtksourceview-2.0/language-specs/
mkdir -p ~/.gnome2/gedit
cp snippets ~/.gnome2/gedit/
