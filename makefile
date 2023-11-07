update:
	git add .
	git commit -m "update"
	git push

push:
	git push

upgrade:
	git stash
	git pull
	python3 main.py