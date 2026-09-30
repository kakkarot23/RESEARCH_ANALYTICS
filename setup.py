from setuptools import setup, find_packages

setup(
    name="tellco_analytics",
    version="1.0.0",
    author="Telecom Analytics Team",
    author_email="analytics@tellco.com",
    description="User Analytics in Telecommunication Industry - Overview, Engagement, Experience & Satisfaction Analysis",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "scipy",
        "sqlalchemy",
        "streamlit",
        "pytest",
        "matplotlib",
        "seaborn"
    ],
)
