# coding=utf8
import json
import sys
sys.path.append(".")


def process_arguments():
    if len(sys.argv) < 2:
        print('missing argument target')
        sys.exit(1)
    try:
        mod, filed = sys.argv[1].split(':')
        return mod, filed
    except ValueError:
        print('invalid argument target( model:class name )')
        sys.exit(1)


def import_class():
    mod_name, field_name = process_arguments()
    mod = __import__(mod_name)
    class_obj = getattr(mod, field_name)
    ins = class_obj()
    format_class(field_name, json.loads(ins.json()))


def detectType(obj):
    if isinstance(obj, str):
        return "String"
    if isinstance(obj, type(1)):
        return "int"
    if isinstance(obj, type(True)):
        return "bool"

def format_class(class_name, obj):
    fields = list(obj.keys())
    const_rows = [f"{fd.upper()}KEY" for fd in fields]
    lines = []
    lines.append('class %s {' % class_name)
    lines.append("  // consts fields")
    for filed_name, const_name in zip(fields, const_rows):
        lines.append(f'  static const {const_name} = "{filed_name}";')
    lines.append("")
    for field_name in fields:
        lines.append(f"  {detectType(obj[field_name])} _{field_name};")
        lines.append(f"  {detectType(obj[field_name])} get {field_name} => _{field_name};")
        lines.append("  set %s(%s value) {" % (field_name, detectType(obj[field_name])))
        lines.append(f"    _{field_name} = value;")
        lines.append("  }")
    lines.append("")
    lines.append("  // constructors")
    params = ", ".join([f"this._{fd}" for fd in fields])
    lines.append(f"  {class_name}({params});")
    lines.append(f"  {class_name}.fromMap(Map map):")
    constractor_fields = ", ".join(
        [f"_{filed_name} = map[{const_name}]" for filed_name, const_name in zip(fields, const_rows)])
    lines.append(f"      {constractor_fields};")
    lines.append("")
    lines.append("  Map asMap(){")
    json_str = ", ".join(
        [f"{const_name}:_{filed_name}" for filed_name, const_name in zip(fields, const_rows)])
    lines.append("    return {%s};" % json_str)
    lines.append("  }")
    lines.append("}")
    print("\n\n")
    print("\n".join(lines))


def main():
    import_class()


if __name__ == '__main__':
    main()
