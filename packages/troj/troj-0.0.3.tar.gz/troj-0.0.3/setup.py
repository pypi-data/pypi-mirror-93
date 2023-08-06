import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="troj",
    version="0.0.3",
    author="TrojAI",
    author_email="stan.petley@troj.ai",
    description="TrojAI provides the troj Python convenience package to allow users to integrate TrojAI adversarial protections and robustness metrics seamlessly into their AI development pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://troj.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)