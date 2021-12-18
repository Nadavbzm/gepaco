build-all:
	cd frontend && flutter build web
	rm -rf backend/gepaco/static/*
	cp -r frontend/build/web/* backend/gepaco/static
	cd backend && python setup.py bdist_wheel
