from importlib.machinery import SourceFileLoader
from hydration import scalars, helpers, Struct
from struct_handling import load_structs_from_path

hydration_scalar_to_str = {
    scalars.UInt8: "uint8",
    scalars.UInt16: "uint16",
    scalars.UInt32: "uint32",
    scalars.UInt64: "uint64",
    scalars.Int8: "int8",
    scalars.Int16: "int16",
    scalars.Int32: "int32",
    scalars.Int64: "int64",
}

class HydrationStructsParser():

    def __init__(self, hydration_structs_file: str) -> None:
        self.structs_file = hydration_structs_file

    def run(self) -> dict:
        icd = SourceFileLoader("icd", self.structs_file).load_module()
        messages_dict = {}
        messages_dict["messages"] = []
        for struct_name, struct in load_structs_from_path(self.structs_file).items():
            struct_field_names = struct.__dict__["_field_names"]
            struct_fields = struct.__dict__
            struct_json = {
                
                "name": struct_name,
            }
            struct_json["fields"] = self._generate_struct_fields(struct)
            messages_dict["messages"].append(struct_json)

        return messages_dict    

    def _generate_struct_fields(self, struct):
        assert isinstance(helpers.as_obj(struct), Struct)
        fields = []
        for field_name in struct.__dict__["_field_names"]:
            field = struct.__dict__[field_name]
            if isinstance(helpers.as_obj(field), Struct):
                fields.append({
                    "name": field_name,
                    "type": "nested",
                    "typeName": type(field).__name__,
                    "fields": self._generate_struct_fields(type(field))
                })
            try:
                field_type = hydration_scalar_to_str[type(field)]
            except KeyError:
                try:
                    field_type = hydration_scalar_to_str[type(field.data_field)]
                except:
                    field_type = "bytes"
            fields.append({
                "name": field_name,
                "size": field.size,
                "endiannes": "le",
                "type": field_type
            })
        return fields
        