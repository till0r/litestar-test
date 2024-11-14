# Run the app
DEBUG=true PORT=8000 litestar run  --reload

# Run tets
coverage run -m pytest -v
