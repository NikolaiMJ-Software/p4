import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from test.type_check.it_test import typecheck_test

'''
-----------------
Passing unit test for the type checker
-----------------
'''
def test_struct_get_parrent():
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        CreateStruct(   # Return = None
            "Warrior", (
                "Character",
                []
            )
        ),
        Var("Health", "Warrior")    # Return = "int"
    ]
    
    res = []
    check = TypeCheckerVisitor()
    for n in node: 
        res.append(check.visit(n))
    
    assert [None, None, "int"] == res
    
def test_struct_overwrite():
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        CreateStruct(   # Return = None
            "Warrior", (
                "Character",
                [CreateVariable("Health", StringLiteral("100"))]
            )
        ),
        Var("Health", "Warrior"),   # Return = "str"
        Var("Health", "Character")  # Return = "int"
    ]
    
    res = []
    check = TypeCheckerVisitor()
    for n in node: 
        res.append(check.visit(n))
    assert [None, None, "str", "int"] == res

def test_struct_get_var():
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        CreateStruct(   # Return = None
            "Warrior", (
                "Character",
                [CreateVariable("Defense", FloatLiteral(4.7))]
            )
        ),
        CreateVariable("X", Add(Var("Defense", "Warrior"), Var("Health", "Warrior")))   # Return = "float"
    ]
    
    res = []
    check = TypeCheckerVisitor()
    for n in node: 
        res.append(check.visit(n))
    assert [None, None, "float"] == res
    
def test_struct_change_var():
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        CreateStruct(   # Return = None
            "Warrior", (
                "Character",
                [CreateVariable("Defense", FloatLiteral(4.7))]
            )
        ),
        Assign("Health", "Warrior", IntLiteral(120))    # Return = "int"
    ]
    
    res = []
    check = TypeCheckerVisitor()
    for n in node: 
        res.append(check.visit(n))
    assert [None, None, "int"] == res

def test_struct_get_and_change_var():
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100)),
                CreateVariable("Name", None)]
            )
        ),
        CreateStruct(   # Return = None
            "Warrior", (
                "Character",
                [CreateVariable("Defense", FloatLiteral(4.7))]
            )
        ),
        CreateStruct(   # Return = None
            "Knight", (
                "Warrior",
                [CreateVariable("Speed", Neg(IntLiteral(2)))]
            )
        ),
        CreateStruct(   # Return = None
            "Hero", 
            ("Warrior", [])
        ),
        CreateStruct(   # Return = None
            "Enemy", 
            ("Warrior", [])
        ),
        Var("Name", "Hero"),    # Return = None
        Var("Name", "Enemy"),   # Return = None
        Assign("Name", "Hero", StringLiteral("Bob")),   # Return = "str"
        Var("Name", "Hero"),    # Return = "str"
        Var("Name", "Enemy"),   # Return = None
    ]
    
    res = []
    check = TypeCheckerVisitor()
    for n in node: 
        res.append(check.visit(n))
    assert [None, None, None, None, None, None, None, "str", "str", None] == res

'''
-----------------
Failing unit test for the type checker
-----------------
'''
def test_struct_duplicate_name():
    struct_name = "Warrior"
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        CreateStruct(   # Return = None
            struct_name, (
                "Character",
                []
            )
        ),
        CreateStruct(   # Raise = TypeError
            struct_name, (
                "Character",
                []
            )
        )
    ]
    check = TypeCheckerVisitor()
    with pytest.raises(TypeError) as exc_info:
        for n in node: 
            check.visit(n)
    assert str(exc_info.value) == f"The struct: '{struct_name}' already exist"
    
def test_struct_undefined_parrent():
    undefined_parrent = "Warrior"
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        CreateStruct(
            "Knight", (
                undefined_parrent,  # Raise = TypeError
                []
            )
        )
    ]
    check = TypeCheckerVisitor()
    with pytest.raises(TypeError) as exc_info:
        for n in node: 
            check.visit(n)
    assert str(exc_info.value) == f"The parrent struct: '{undefined_parrent}' don't exist"
    
def test_struct_undefined_struct():
    undefined_struct = "Warrior"
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        Var("Health", undefined_struct)    # Raise = TypeError
    ]
    check = TypeCheckerVisitor()
    with pytest.raises(TypeError) as exc_info:
        for n in node: 
            check.visit(n)
    assert str(exc_info.value) == f"The struct: '{undefined_struct}' are not defined"

def test_struct_undefined_var():
    var_name = "Defense"
    node = [
        CreateStruct(   # Return = None
            "Character", (
                None,
                [CreateVariable("Health", IntLiteral(100))]
            )
        ),
        Var(var_name, "Character")  # Raise = TypeError
    ]
    check = TypeCheckerVisitor()
    with pytest.raises(TypeError) as exc_info:
        for n in node: 
            check.visit(n)
    assert str(exc_info.value) == f"The variable: '{var_name}' are not defined in the struct: 'Character'"

'''
-----------------
Passing integration test for the type checker
-----------------
'''
def test_it_pass_struct_get_parrent():
    get_parrent = typecheck_test(get_parrent_code)
    assert [None, None] == get_parrent
get_parrent_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    
"""

def test_it_pass_struct_overwrite():
    overwrite = typecheck_test(overwrite_parrent_var_code)
    assert [None, None, None, None, None] == overwrite
overwrite_parrent_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
"""

def test_it_pass_struct_get_var():
    get_var = typecheck_test(get_var_code)
    assert [None, None, None, None, None, "int"] == get_var
get_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
Health from Enemy
"""    

def test_it_pass_struct_change_var():
    change_var = typecheck_test(change_var_code)
    assert [None, None, None, None, None, "int"] == change_var
change_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
Health from Enemy is Health from Enemy - Attack from Me
"""

def test_it_pass_struct_get_and_change_var():
    change_name_res = typecheck_test(change_name_code)
    assert [None, None, None, None, None, None, None, "str", "str", None] == change_name_res
change_name_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
Name from Enemy
Name from Me
Name from Enemy is "Bob"
Name from Enemy
Name from Me
"""

'''
-----------------
Failing integration test for the type checker
-----------------
'''
def test_it_fail_struct_duplicate_name():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(duplicate_struct_name_code)
    assert str(exc_info.value) == "The struct: 'Character' already exist"
duplicate_struct_name_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Character with:
    Speed
"""    

def test_it_fail_struct_undefined_parrent():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(wrong_parrent_code)
    assert str(exc_info.value) == "The parrent struct: 'Person' don't exist"
wrong_parrent_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Person with:
    Attack is 3
    Defense is 2
"""    

def test_it_fail_struct_undefined_struct():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(accing_undefined_struct_code)
    assert str(exc_info.value) == "The struct: 'Enemy' are not defined"
accing_undefined_struct_code = """Health from Enemy
"""    

def test_it_fail_struct_undefined_var():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(undefined_var_code)
    assert str(exc_info.value) == "The variable: 'Speed' are not defined in the struct: 'Character'"
undefined_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
Speed from Character
"""