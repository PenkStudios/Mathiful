run:
	cd src && python main.py

compile:
	wine pyinstaller --icon=src/app.ico --onefile --noconsole src/main.py
	cp -r src/resources/* ./dist/resources/

crossdep:
	wine python -m pip install pygame
	wine python -m pip install pyinstaller
