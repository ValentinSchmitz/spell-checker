<p align="center"><img src="https://github.com/ValentinSchmitz/spell-checker/assets/72657531/95e213f6-87d7-477f-877e-b55aa7ed44c4"></p>
<h1 align="center">Spell Checker for Anki</h1>

<p align="center">
<a title="Latest (pre-)release" href="https://github.com/ValentinSchmitz/spell-checker/releases"><img src ="https://img.shields.io/github/downloads-pre/ValentinSchmitz/spell-checker/latest/totalcolorB=brightgreen"></a>
<a title="License: GNU AGPLv3" href="https://github.com/ValentinSchmitz/spell-checker/blob/main/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>

  
Welcome to Spell Checker for Anki! This add-on enhances your Anki flashcard experience by ensuring your entries are error-free. The spell-checker identifies and lets you correct spelling mistakes in multiple languages, seamlessly integrating into the Anki interface. You can add your own words via the integrated personal dictionary.

### Installation

#### AnkiWeb

The easiest way to install Spell Checker is through [AnkiWeb]().

#### Manual installation

1. Download the latest `.ankiaddon` file from the [releases tab](https://github.com/ValentinSchmitz/spell-checker/releases).
2. Open the folder where your downloads are located and double-click on the downloaded `.ankiaddon` file.
3. Follow the installation prompt and restart Anki if it asks you to.

### Setup

#### Basic

The Add-on is able to download dictionary files for all main languages. To activate your language:

1. On the main page, go to *Tools > Dictionary configuration.*
2. Choose your desired language(s) from the list and click *Enable*.
3. Once the list items turn green, the language is successfully downloaded.

You can disable languages by selecting them and clicking *Disable*.

#### Custom dictionaries

You can simply right-click on words and then choose *Add to dictionary*, to save custom words. If you have a more extensive word list, you can integrate them in the following ways:

##### `.txt` files

You should have a `.txt` file, which consists of one word per line.

1.  On the main page, go to *Tools > Dictionary configuration.*
2. Start by clicking on *Open Personal Dictionary Folder*. Once the specific folder opens, please transfer the `.txt` file into this folder.
3. Go back to the *Dictionary configuration* screen and click the button *Compile your dictionaries.*
4. Your dictionary should appear in the list. You may have to reopen the configuration window. 

##### `.dic` files

If you have a `.dic` file with the accompanying `.aff` file, you can proceed the same way as described for the .txt files. If you do not supply a .aff file, a clear one with no additional rules is created.

##### `.bdic` files

If you have a precompiled `.bdic` file, proceed as follows:

1.  On the main page, go to *Tools > Dictionary configuration.*
2. Start by clicking on *Open .bdic folder.* Once the specific folder opens, please transfer the .bdic file into this folder.
3. Your dictionary should appear in the list. You may have to reopen the configuration window. 

### License and Credits

This project is based on the legacy plugin [Spelling Police](<https://github.com/lovac42/SpellingPolice>) by [lovac42](<https://github.com/lovac42>).

The binaries for the .bidc conversion are downloaded from jankelmen's project [convert-dict-tool-from-chromium](<https://github.com/jankelemen/convert-dict-tool-from-chromium>).

The dictionaries are provided by [dictionaries](<https://github.com/wooorm/dictionaries>) from wooorm. See their repository for specific licenses. You can also report errors in the dictionaries there.

The plugin icon is created by  <a href="<https://github.com/carbon-design-system/carbon?ref=svgrepo.com>" target="\_blank">Carbon Design</a> in Apache License via <a href="<https://www.svgrepo.com/>" target="\_blank">SVG Repo</a>.
