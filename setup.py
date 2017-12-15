import os
import sys
import hashlib
import urllib.request
import subprocess
from setuptools import setup, find_packages

kenja_version = '3.0-alpha'
data_files = [("kenja", ["kenja/readme_for_historage.txt"])]


def validate_md5sum(digest, path):
    return digest == hashlib.md5(open(path, 'rb').read()).hexdigest()


class JavaParserInstaller:
    parser_path = 'kenja/lib/java/java-parser.jar'
    parser_location = 'https://github.com/niyaton/kenja-java-parser/releases/download/0.5/kenja-java-parser-0.5-jar-with-dependencies.jar'
    parser_digest = '3686529db9d36d5ef5d7425692d95aea'

    def validate_parser(self):
        if not os.path.exists(self.parser_path):
            return 'not installed'

        if not validate_md5sum(self.parser_digest, self.parser_path):
            return 'invalid parser'
        return 'installed'

    def get_confirm_text(self, status):
        if status == 'not installed':
            return "{0} does not exist. Do you want to download it?[y/n]".format(self.parser_path)
        elif status == 'invalid parser':
            return "{0} is different from designated parser script. Do you want to overwrite it?[y/n]".format(self.parser_path)
        else:
            return ""

    def ask_yesno(self, confirm_text):
        print(confirm_text)
        choice = input().lower()
        yes = set(['yes', 'y', 'ye'])
        return choice in yes

    def install_parser(self):
        install_status = self.validate_parser()
        if install_status == 'installed':
            return True

        if not self.ask_yesno(self.get_confirm_text(install_status)):
            return install_status != 'not installed'

        self.download_parser()
        install_status = self.validate_parser()

        if self.validate_parser() != 'installed':
            print("md5 hash of {0} is incorrect! remove it and tryagain.".format(self.parser_path))
            sys.exit(1)
        return True

    def download_parser(self):
        with open(self.parser_path, 'wb') as f:
            with urllib.request.urlopen(self.parser_location) as response:
                f.write(response.read())


def copy_java_parser():
    installer = JavaParserInstaller()
    if installer.install_parser():
        data_files.append(("kenja/lib/java", ["kenja/lib/java/java-parser.jar"]))
    else:
        print("java parser will not be installed.")
        print("You should disable java parser when you run kenja")


copy_java_parser()

setup(name='kenja',
      version='3.0',
      description='A Historage Converter',
      author='Kenji Fujiwara',
      author_email='fujiwara@toyota-ct.ac.jp',
      url='https://github.com/niyaton/kenja',
      packages=find_packages(),
      data_files=data_files,
      entry_points={
          'console_scripts': [
              'kenja.historage.convert = kenja.convert:convert',
              'kenja.historage.parse = kenja.convert:parse',
              'kenja.historage.construct = kenja.convert:construct',
              'kenja.debug.check_duplicate_entry = kenja.git.detect_duplicate_entry:main',
              'kenja.debug.check_historage_equivalence = kenja.git.diff:main'
          ]
      },
      install_requires=[
          "GitPython==2.1.8",
      ],
      license="MIT license",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Science/Resarch',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Java',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities'
      ]
      )
