from setuptools import setup

setup(name='instrumentserver',
      version='0.0.1',
      description='TBD',
      url='https://github.com/toolsforexperiments/instrumentserver',
      author='Wolfgang Pfaff',
      author_email='wolfgangpfff@gmail.com',
      license='MIT',
      packages=['instrumentserver'],
      zip_safe=False,
      entry_points={"console_scripts": [
            "instrumentserver = instrumentserver.apps:serverScript",
            "instrumentserver-param-manager = instrumentserver.apps:parameterManagerScript",
            "instrumentserver-dashboard = instrumentserver.apps:bokehDashboard",
            "instrumentserver-dashboardlogger = instrumentserver.apps:loggerAndDashboard"]}
      )
