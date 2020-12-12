
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programleftADDSUBleftMULDIVMODADD ASSIGNMENT BEGIN COLON COMMA DECLARE DIV DO DOWNTO ELSE END ENDFOR ENDIF ENDWHILE EQUALS FOR FROM GEQ GREATER IF LEFT_BRACKET LEQ LOWER MOD MUL NOT_EQUALS NUM READ REPEAT RIGHT_BRACKET SEMICOLON SUB THEN TO UNTIL WHILE WRITE pidentifierprogram : DECLARE declarations BEGIN commands END\n               | BEGIN commands ENDdeclarations : declarations COMMA pidentifier\n                    | declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKETdeclarations : pidentifierdeclarations : pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKETcommands : commands command\n                | commandcommand : identifier ASSIGNMENT expression SEMICOLON\n               | IF condition THEN commands ELSE commands ENDIF\n               | IF  condition  THEN  commands  ENDIF\n               | WHILE  condition  DO  commands  ENDWHILE\n               | REPEAT  commands  UNTIL  condition SEMICOLON\n               | FOR  pidentifier  FROM  value TO  value DO  commands  ENDFOR\n               | FOR  pidentifier  FROM  value  DOWNTO  value DO  commands  ENDFOR\n               | READ  identifier SEMICOLON\n               | WRITE  value SEMICOLONexpression : value\n                  | value ADD value\n                  | value SUB value\n                  | value MUL value\n                  | value DIV value\n                  | value MOD valuecondition : value EQUALS value\n                 | value NOT_EQUALS value\n                 | value LOWER value\n                 | value GREATER value\n                 | value LEQ value\n                 | value GEQ valuevalue : NUM\n             | identifieridentifier : pidentifier\n                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKETidentifier : pidentifier LEFT_BRACKET NUM RIGHT_BRACKET'
    
_lr_action_items = {'DECLARE':([0,],[2,]),'BEGIN':([0,4,5,33,86,94,],[3,16,-5,-3,-6,-4,]),'$end':([1,19,51,],[0,-2,-1,]),'pidentifier':([2,3,6,7,9,10,11,12,14,15,16,17,20,21,27,29,32,37,38,39,40,41,42,43,44,45,46,49,50,54,55,56,57,58,59,60,67,79,80,81,82,83,84,87,91,92,93,95,96,97,98,],[5,13,13,-8,13,13,13,28,13,13,13,33,-7,13,13,47,13,13,13,13,13,13,13,13,13,13,13,-16,-17,-9,13,13,13,13,13,13,13,13,-11,-12,-13,13,13,13,-10,13,13,13,13,-14,-15,]),'IF':([3,6,7,11,16,20,27,32,37,44,49,50,54,60,67,79,80,81,82,87,91,92,93,95,96,97,98,],[9,9,-8,9,9,-7,9,9,9,9,-16,-17,-9,9,9,9,-11,-12,-13,9,-10,9,9,9,9,-14,-15,]),'WHILE':([3,6,7,11,16,20,27,32,37,44,49,50,54,60,67,79,80,81,82,87,91,92,93,95,96,97,98,],[10,10,-8,10,10,-7,10,10,10,10,-16,-17,-9,10,10,10,-11,-12,-13,10,-10,10,10,10,10,-14,-15,]),'REPEAT':([3,6,7,11,16,20,27,32,37,44,49,50,54,60,67,79,80,81,82,87,91,92,93,95,96,97,98,],[11,11,-8,11,11,-7,11,11,11,11,-16,-17,-9,11,11,11,-11,-12,-13,11,-10,11,11,11,11,-14,-15,]),'FOR':([3,6,7,11,16,20,27,32,37,44,49,50,54,60,67,79,80,81,82,87,91,92,93,95,96,97,98,],[12,12,-8,12,12,-7,12,12,12,12,-16,-17,-9,12,12,12,-11,-12,-13,12,-10,12,12,12,12,-14,-15,]),'READ':([3,6,7,11,16,20,27,32,37,44,49,50,54,60,67,79,80,81,82,87,91,92,93,95,96,97,98,],[14,14,-8,14,14,-7,14,14,14,14,-16,-17,-9,14,14,14,-11,-12,-13,14,-10,14,14,14,14,-14,-15,]),'WRITE':([3,6,7,11,16,20,27,32,37,44,49,50,54,60,67,79,80,81,82,87,91,92,93,95,96,97,98,],[15,15,-8,15,15,-7,15,15,15,15,-16,-17,-9,15,15,15,-11,-12,-13,15,-10,15,15,15,15,-14,-15,]),'COMMA':([4,5,33,86,94,],[17,-5,-3,-6,-4,]),'LEFT_BRACKET':([5,13,33,],[18,29,52,]),'END':([6,7,20,32,49,50,54,80,81,82,91,97,98,],[19,-8,-7,51,-16,-17,-9,-11,-12,-13,-10,-14,-15,]),'UNTIL':([7,20,27,49,50,54,80,81,82,91,97,98,],[-8,-7,45,-16,-17,-9,-11,-12,-13,-10,-14,-15,]),'ELSE':([7,20,49,50,54,60,80,81,82,91,97,98,],[-8,-7,-16,-17,-9,79,-11,-12,-13,-10,-14,-15,]),'ENDIF':([7,20,49,50,54,60,80,81,82,87,91,97,98,],[-8,-7,-16,-17,-9,80,-11,-12,-13,91,-10,-14,-15,]),'ENDWHILE':([7,20,49,50,54,67,80,81,82,91,97,98,],[-8,-7,-16,-17,-9,81,-11,-12,-13,-10,-14,-15,]),'ENDFOR':([7,20,49,50,54,80,81,82,91,95,96,97,98,],[-8,-7,-16,-17,-9,-11,-12,-13,-10,97,98,-14,-15,]),'ASSIGNMENT':([8,13,70,71,],[21,-32,-33,-34,]),'NUM':([9,10,15,18,21,29,38,39,40,41,42,43,45,46,52,53,55,56,57,58,59,83,84,85,],[24,24,24,34,24,48,24,24,24,24,24,24,24,24,72,73,24,24,24,24,24,24,24,90,]),'EQUALS':([13,23,24,25,70,71,],[-32,38,-30,-31,-33,-34,]),'NOT_EQUALS':([13,23,24,25,70,71,],[-32,39,-30,-31,-33,-34,]),'LOWER':([13,23,24,25,70,71,],[-32,40,-30,-31,-33,-34,]),'GREATER':([13,23,24,25,70,71,],[-32,41,-30,-31,-33,-34,]),'LEQ':([13,23,24,25,70,71,],[-32,42,-30,-31,-33,-34,]),'GEQ':([13,23,24,25,70,71,],[-32,43,-30,-31,-33,-34,]),'SEMICOLON':([13,24,25,30,31,35,36,61,62,63,64,65,66,68,70,71,74,75,76,77,78,],[-32,-30,-31,49,50,54,-18,-24,-25,-26,-27,-28,-29,82,-33,-34,-19,-20,-21,-22,-23,]),'ADD':([13,24,25,36,70,71,],[-32,-30,-31,55,-33,-34,]),'SUB':([13,24,25,36,70,71,],[-32,-30,-31,56,-33,-34,]),'MUL':([13,24,25,36,70,71,],[-32,-30,-31,57,-33,-34,]),'DIV':([13,24,25,36,70,71,],[-32,-30,-31,58,-33,-34,]),'MOD':([13,24,25,36,70,71,],[-32,-30,-31,59,-33,-34,]),'THEN':([13,22,24,25,61,62,63,64,65,66,70,71,],[-32,37,-30,-31,-24,-25,-26,-27,-28,-29,-33,-34,]),'DO':([13,24,25,26,61,62,63,64,65,66,70,71,88,89,],[-32,-30,-31,44,-24,-25,-26,-27,-28,-29,-33,-34,92,93,]),'TO':([13,24,25,69,70,71,],[-32,-30,-31,83,-33,-34,]),'DOWNTO':([13,24,25,69,70,71,],[-32,-30,-31,84,-33,-34,]),'FROM':([28,],[46,]),'COLON':([34,72,],[53,85,]),'RIGHT_BRACKET':([47,48,73,90,],[70,71,86,94,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declarations':([2,],[4,]),'commands':([3,11,16,37,44,79,92,93,],[6,27,32,60,67,87,95,96,]),'command':([3,6,11,16,27,32,37,44,60,67,79,87,92,93,95,96,],[7,20,7,7,20,20,7,7,20,20,7,20,7,7,20,20,]),'identifier':([3,6,9,10,11,14,15,16,21,27,32,37,38,39,40,41,42,43,44,45,46,55,56,57,58,59,60,67,79,83,84,87,92,93,95,96,],[8,8,25,25,8,30,25,8,25,8,8,8,25,25,25,25,25,25,8,25,25,25,25,25,25,25,8,8,8,25,25,8,8,8,8,8,]),'condition':([9,10,45,],[22,26,68,]),'value':([9,10,15,21,38,39,40,41,42,43,45,46,55,56,57,58,59,83,84,],[23,23,31,36,61,62,63,64,65,66,23,69,74,75,76,77,78,88,89,]),'expression':([21,],[35,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> DECLARE declarations BEGIN commands END','program',5,'p_program','code_parser.py',125),
  ('program -> BEGIN commands END','program',3,'p_program','code_parser.py',126),
  ('declarations -> declarations COMMA pidentifier','declarations',3,'p_declarations_muliple','code_parser.py',129),
  ('declarations -> declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET','declarations',8,'p_declarations_muliple','code_parser.py',130),
  ('declarations -> pidentifier','declarations',1,'p_declarations_single_var','code_parser.py',140),
  ('declarations -> pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET','declarations',6,'p_declarations_single_tab','code_parser.py',151),
  ('commands -> commands command','commands',2,'p_commands','code_parser.py',164),
  ('commands -> command','commands',1,'p_commands','code_parser.py',165),
  ('command -> identifier ASSIGNMENT expression SEMICOLON','command',4,'p_command','code_parser.py',167),
  ('command -> IF condition THEN commands ELSE commands ENDIF','command',7,'p_command','code_parser.py',168),
  ('command -> IF condition THEN commands ENDIF','command',5,'p_command','code_parser.py',169),
  ('command -> WHILE condition DO commands ENDWHILE','command',5,'p_command','code_parser.py',170),
  ('command -> REPEAT commands UNTIL condition SEMICOLON','command',5,'p_command','code_parser.py',171),
  ('command -> FOR pidentifier FROM value TO value DO commands ENDFOR','command',9,'p_command','code_parser.py',172),
  ('command -> FOR pidentifier FROM value DOWNTO value DO commands ENDFOR','command',9,'p_command','code_parser.py',173),
  ('command -> READ identifier SEMICOLON','command',3,'p_command','code_parser.py',174),
  ('command -> WRITE value SEMICOLON','command',3,'p_command','code_parser.py',175),
  ('expression -> value','expression',1,'p_expression','code_parser.py',183),
  ('expression -> value ADD value','expression',3,'p_expression','code_parser.py',184),
  ('expression -> value SUB value','expression',3,'p_expression','code_parser.py',185),
  ('expression -> value MUL value','expression',3,'p_expression','code_parser.py',186),
  ('expression -> value DIV value','expression',3,'p_expression','code_parser.py',187),
  ('expression -> value MOD value','expression',3,'p_expression','code_parser.py',188),
  ('condition -> value EQUALS value','condition',3,'p_condition','code_parser.py',205),
  ('condition -> value NOT_EQUALS value','condition',3,'p_condition','code_parser.py',206),
  ('condition -> value LOWER value','condition',3,'p_condition','code_parser.py',207),
  ('condition -> value GREATER value','condition',3,'p_condition','code_parser.py',208),
  ('condition -> value LEQ value','condition',3,'p_condition','code_parser.py',209),
  ('condition -> value GEQ value','condition',3,'p_condition','code_parser.py',210),
  ('value -> NUM','value',1,'p_value','code_parser.py',213),
  ('value -> identifier','value',1,'p_value','code_parser.py',214),
  ('identifier -> pidentifier','identifier',1,'p_identifier','code_parser.py',218),
  ('identifier -> pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET','identifier',4,'p_identifier','code_parser.py',219),
  ('identifier -> pidentifier LEFT_BRACKET NUM RIGHT_BRACKET','identifier',4,'p_identifier_tab','code_parser.py',223),
]
