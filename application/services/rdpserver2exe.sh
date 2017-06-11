#to Convert rdpviperserver.py to exe run commands below

echo "Generating rdpviperserver.exe"

read -n 1 -s -p "Press any key to continue"

echo "Generating rdpviperserver.exe"

# wine ~/.wine/drive_c/Python27/Scripts/pyinstaller.exe --onefile HelloWorld.py

wine pyinstaller --onefile --noconsole --nowindowed rdpviperserver.py
rm -rf build/
rm -rf dist/
sed -i 's/console=True/console=False/g' rdpviperserver.spec
wine pyinstaller rdpviperserver.spec
cp dist/rdpviperserver.exe .
cp dist/rdpviperserver.exe /var/www/html/
cp dist/rdpviperserver.exe ../../www/html/
cp dist/rdpviperserver.exe .
rm -rf build/
rm -rf dist/
rm -rf rdpviperserver.spec
cd ../

echo "Good now go and deploy it and try to connect with the client"