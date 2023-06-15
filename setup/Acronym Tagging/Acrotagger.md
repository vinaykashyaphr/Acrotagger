<h1 align="center">Acrotagger</h1>
<p align="center">An application to add or remove acronym elements in data modules.</p>

<p align="center">
    <img src="images\interface_AT.png" alt="Empty interface">
</p>

## Installation

1. Double click "Acrotagger_setup.exe".
2. Enter the password in "Password: " label.
3. The installation folder will be defaultly set to local user program folder, but user can change the path as shown.
4. after setting installation path, click on "Next".
5. Check in the "Create a desktop shortcut" if needed.
6. Click "Next" and then "Install" to install the application.

<p align="center">
    <img src="images\at_password.png" alt="Installation"></p>
<p align="center">
    <img src="images\at_location.png" alt="Installation">
</p>
<p align="center">
    <img src="images\at_desktopicon.png" alt="Installation">
<p align="center">
    <img src="images\at_install.png" alt="Installation">

## Getting Started

### Prerequisites

#### catalog

> To support each sub applications of DME Configurator, the "catalog" directory should be present in the local drive "C:" directly.

## Usage and description

### Usage

1. The application includes 2 sub processes namely,`<br>` i.   Tagging acronym elements `<br>` ii.  Removing acronyms elements`<br>`
2. Authors can use the processes as per their convenience in authoring process.
3. The application only tags the acronym mentioned in the table in a dmc with title as "List of Acronyms and Abbreviations".
4. The application only supports to edit ATA specific DMCs. No generic modules will be edited including local or common repositories.

### Description

1. Tagging acronym elements:

   - Refreshes the DMCs for general xml declaration attributes.
   - Generates and adds acronym elements for each acronyms mentioned in the given acronym table.
   - All the previously tagged acronym elements will be removed before continuing.
   - The acronyms will not be tagged in the DMC in which acronym input table was kept.
   - Creates no log file, since the application has multiple triggers between different excecutables.

   <p align="center">
       <img src="images\acronym_add.png" alt="Installation">

   <p align="center">
       <img src="images\at_input.png" alt="Installation">
2. Removing acronym elements:

   - Removes the acronym elements if previously tagged everywhere in each DMC within working folder.

> NOTE:
>
> 1. The modification happens within the working folder itself. The "temp_folder" and "acro_output" directories will be discarded automatically after completion of the process.
> 2. No lower-case or single alphabet are allowed in the input acronym table. The acronyms with a group of capitalized alphabets has to be given as abbreviation.
> 3. Keep a backup copy of the working folder before performing any atomization process.
> 4. The application is only compatible for S1000D 4-1 issue.

### Tagging Format

| Instance                  | Tagging Format                                                                                                                           | Example                                                                                                                      |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| First Instance Within DMC | "`<acronym id="acro-[0-9]{4}"><acronymTerm>(abbreviation)</acronymTerm><acronymDefinition>(definition)</acronymDefinition></acronym>`" | `<acronym id="acro-0005"><acronymTerm>TR</acronymTerm><acronymDefinition>temporary revision</acronymDefinition></acronym>` |
| Other Instances           | "`<acronymTerm internalRefId="(given id at first instance)">(abbreviation)</acronymTerm>`"                                             | `<acronymTerminternalRefId="acro-0005">TR</acronymTerm>`                                                                   |

> **UPDATES**:
>
> 1. The modification happens within the working folder itself "acro_output" folder won't remain in the directory.
> 2. The "temp_folder" and "acro_output" both directories will be discarded automatically after completion of the process.
> 3. A seperate user interface that allows user to simply drag and drop the input folder.
> 4. Separate function to remove acronyms. This will remove all the acronym elements present in each data module within working folder.
> 5. Less time consumption since it triggers multple functions as different executable thereby uses less space also.

### Summary

#### Description of functions

| Function                | Description                                                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Tag Acronyms            | Creates and adds acronym elements for every instance of acronyms in each data modules by taking given acronym table as reference. |
| Remove Acronym Elements | Removes all previously tagged acronym elements in each DMC thereby only keeping the acronym terms as freetext.                    |
