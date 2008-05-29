#!/bin/sh

killall gedit

# Register rails-related mime types
sudo cp rails.xml /usr/share/mime/packages
sudo update-mime-database /usr/share/mime

# Install syntaxt definitions for erb and yaml
sudo cp erb.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp yaml.lang /usr/share/gtksourceview-2.0/language-specs/

if [ ! -d $HOME/.gnome2/gedit ]
then
  mkdir -p ~/.gnome2/gedit
fi
cp snippets ~/.gnome2/gedit/

if [ ! -d $HOME/.gnome2/gedit/snippets ]
then
  mkdir -p ~/.gnome2/gedit/snippets
fi
cp snippets/* ~/.gnome2/gedit/snippets/

if [ ! -d $HOME/.gnome2/gedit/plugins ]
then
  mkdir -p ~/.gnome2/gedit/plugins
fi
cp -R plugins/* ~/.gnome2/gedit/plugins

if [ ! -d $HOME/.gnome2/gedit/styles ]
then
  mkdir -p ~/.gnome2/gedit/styles
fi
cp -R styles/* ~/.gnome2/gedit/styles
