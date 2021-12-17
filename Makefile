build-all:
	cd frontend && flutter build web
	pwd
	rm -rf backend/GPC/static/*
	cp -r frontend/build/web/* backend/GPC/static
	cd backend && python setup.py bdist_wheel
