# Honeycodeorm

Honeycode ORM provides an Object Relational Model for interaction with Honeycode workbooks. HoneycodeORMBuilder is the 
main file, pass in your workbook name, and a series of classes will be generated in the "orm" folder, one file per
table in your Honeycode workbook. Each file has two classes, one for batch operation, and one that holds and object
that represents a row in your table.

## Documentation

Example Usage of builder:
python3 HoneycodeORMBuilder.py [workbookid]

Output in the ORM folder a list of files representing your tables

## License

This project is licensed under the Apache-2.0 License.

