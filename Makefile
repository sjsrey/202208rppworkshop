cogs:
	docker run --rm \
                -p 4000:4000 \
                -p 8888:8888 \
                --user root \
                -e NB_UID=1000 \
                -e NB_GID=1001 \
                -v ${PWD}:/home/jovyan/work \
				sjsrey/cogs:0.1
