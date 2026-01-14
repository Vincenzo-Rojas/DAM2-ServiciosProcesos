# Actualizar rama profesor

git config --global alias.update-profesor "!git fetch https://github.com/Josemedvel/psp-25-26.git main:profesor-temporal && git checkout profesor && git merge profesor-temporal --allow-unrelated-histories -m 'Actualización desde repo profesor' && git push origin profesor && git branch -d profesor-temporal"
