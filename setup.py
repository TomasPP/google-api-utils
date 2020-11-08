from setuptools import setup


setup(
    name="google_api_util",
    version="1.0.0",
    license="MIT",
    author="Tomas P",
    author_email="ttt@ttt.tt",
    url="...",
    py_modules=["google_api_util"],
    install_requires=[
                      "google-api-python-client>=1.8.2,<=2.0",
                      "google-auth-oauthlib>=0.4.1,<=1.0",
                      "google-auth-httplib2>=0.0.3,<1"
                      ],
    # entry_points={"console_scripts": ["test=test:main"]},
)
