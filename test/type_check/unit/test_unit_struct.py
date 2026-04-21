import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

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
