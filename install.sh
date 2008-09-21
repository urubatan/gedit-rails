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
cp -r snippets ~/.gnome2/gedit/

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

# set Darkmate as default Gedit Theme, It supports Rails specific syntax
# 
# find more gedit themes at http://github.com/mig/gedit-themes
gconftool-2 --set /apps/gedit-2/preferences/editor/colors/scheme  -t string darkmate

# set default plugins
gconftool-2 --set /apps/gedit-2/plugins/active-plugins  -t list --list-type string [line_tools,classbrowser,auto_completion,snapopen,sessionsaver,codecomment,indent,filebrowser,snippets,externaltools]

