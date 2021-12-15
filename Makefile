build-all:
	cd frontend && flutter build web
	pwd
	cp -r frontend/build/web/ backend/GPC/static/
	cd backend && python setup.py bdist_wheel

test:
	