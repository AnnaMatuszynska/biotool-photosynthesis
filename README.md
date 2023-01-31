# Photosynthesis _in silico_: an Interactive Dashboard to Study Photosynthesis using a Computational Model

This is a Teaching Tool in Biology: an ongoing project launched by Sarah Philipps and Anna Matuszynska at the RWTH Aachen University, Germany. Our goal is to provide a teaching tool applicable to the needs of a XXI century students. We want to show you how computational modeling supports the current research in increasing our understanding how the world works, and we have selected photosynthesis as THE processs to demonstrate it with. At the end, photosynthesis is arguably the most important process on Earth! And even though most of us learn about it at some point at shool there is still so much exciting work going on in the topic.

Here, we created an interactive dashboard, aimed at both curious newcomers and more advanced learners. The user can first read basic information about photosynthesis and photoprotection, learn about fluorescence measurements and finally, perform their own experiments using their _in silico_, varying light conditions and creating _in silico_ synthetic strains that, maybe, can produce more oxygen.
With this tool we want to provide an insight into how photosynthesis works and can be described in mathematical terms. Most importantly, we hope you will have fun by playing with it.

### Setting up

We recommend setting up a virtual environment of your choice, e.g. with conda

```bash
conda env create -f environment.yml
conda activate biotoolenvironment
```

### Run the web page

To get the web page running, the following command is used: `streamlit run Start.py`

### Layout

To change something in the layout of one of the pages, the corresponding Python file must be adapted.

Some layout adjustments, mainly related to the design, of the website can be adjusted in the Streamlit folder, in the \
config.toml file.

### Translations and Texts

Texts and the translations are adapted in the .po files in the locals folder. There are the folders with the language \
versions for the two versions. In each subfolder you can find the texts of each page.

To insert a new language, a subfolder with the abbreviation for the language must be inserted in each of the two \
version folders. Copies of the .po files from one of the other language subfolders are then inserted into this folder. \
These can then be filled with the translations.

In order for the new translation to be displayed in the sidebar menu, the language must be added to the Python files \
of all pages under 'language'.

After changes first run:
For the Introduction/Einführung:`msgfmt -o locales/#/*/LC_MESSAGES/base.mo locales/#/*/LC_MESSAGES/base` \
 For the Methods/Messmethode: `msgfmt -o locales/#/*/LC_MESSAGES/b-messmeth.mo locales/#/*/LC_MESSAGES/b-messmeth`\
 For the Data analysis/Daten-Analyse: `msgfmt -o locales/#/*/LC_MESSAGES/b-Analyse.mo locales/#/*/LC_MESSAGES/b-Analyse`\
 For the Plant Memory/Pflanzengedächtnis: `msgfmt -o locales/#/*/LC_MESSAGES/b-brain.mo locales/#/*/LC_MESSAGES/b-brain`\
 with en/de instead of \* for the language and simple/expert instead of # to generate the translations

### Developers

1. Sarah Philipps: main developer, realization of phase 1: working dashboard prototype
2. Anna Matuszynska: conceptualization, supervision of phase 1, mathematical content and light memory
   joined after the phase 1
3. Marvin van Aalst: code clean-up, testing
4. Tobias Pfennig: provision of teaching videos on fluorescence
