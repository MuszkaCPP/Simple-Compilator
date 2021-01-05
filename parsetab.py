
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programleftADDSUBleftMULDIVMODADD ASSIGNMENT BEGIN COLON COMMA DECLARE DIV DO DOWNTO ELSE END ENDFOR ENDIF ENDWHILE EQUALS FOR FROM GEQ GREATER IF LEFT_BRACKET LEQ LOWER MOD MUL NOT_EQUALS NUM READ REPEAT RIGHT_BRACKET SEMICOLON SUB THEN TO UNTIL WHILE WRITE pidentifierprogram : DECLARE declarations BEGIN commands END\n               | BEGIN commands ENDdeclarations : declarations COMMA pidentifier\n                    | declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKETdeclarations : pidentifierdeclarations : pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKETcommands : commands command\n                | commandcommand : READ identifier SEMICOLONcommand : identifier ASSIGNMENT expression SEMICOLONcommand : REPEAT  commands  UNTIL  condition SEMICOLON\n               | FOR  pidentifier  FROM  value TO  value DO  commands  ENDFOR\n               | FOR  pidentifier  FROM  value  DOWNTO  value DO  commands  ENDFORcommand : WHILE while_occured condition  DO  commands  ENDWHILEwhile_occured :command : IF if_occured condition THEN commands ELSE else_occured commands ENDIFelse_occured :command : IF if_occured condition  THEN  commands  ENDIFif_occured :command : WRITE value SEMICOLONexpression : valueexpression : value ADD value\n                  | value SUB value\n                  | value MUL value\n                  | value DIV value\n                  | value MOD valuecondition : value EQUALS value\n                 | value NOT_EQUALS value\n                 | value LOWER value\n                 | value GREATER value\n                 | value LEQ value\n                 | value GEQ valuevalue : NUMvalue : identifieridentifier : pidentifier\n                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKETidentifier : pidentifier LEFT_BRACKET NUM RIGHT_BRACKET'
    
_lr_action_items = {'DECLARE':([0,],[2,]),'BEGIN':([0,4,5,32,85,95,],[3,16,-5,-3,-6,-4,]),'$end':([1,19,45,],[0,-2,-1,]),'pidentifier':([2,3,6,7,8,10,11,13,14,15,16,17,20,22,23,25,26,27,31,34,37,38,44,48,49,50,51,52,53,58,59,60,61,62,63,64,65,73,74,75,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[5,12,12,-8,12,12,24,-15,-19,12,12,32,-7,12,12,39,12,12,12,-9,12,12,-20,-10,12,12,12,12,12,12,12,12,12,12,12,12,12,-11,12,12,12,12,-14,-17,-18,12,12,12,12,12,12,-12,-13,-16,]),'READ':([3,6,7,10,16,20,23,31,34,44,48,58,65,73,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[8,8,-8,8,8,-7,8,8,-9,-20,-10,8,8,-11,8,8,-14,-17,-18,8,8,8,8,8,8,-12,-13,-16,]),'REPEAT':([3,6,7,10,16,20,23,31,34,44,48,58,65,73,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[10,10,-8,10,10,-7,10,10,-9,-20,-10,10,10,-11,10,10,-14,-17,-18,10,10,10,10,10,10,-12,-13,-16,]),'FOR':([3,6,7,10,16,20,23,31,34,44,48,58,65,73,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[11,11,-8,11,11,-7,11,11,-9,-20,-10,11,11,-11,11,11,-14,-17,-18,11,11,11,11,11,11,-12,-13,-16,]),'WHILE':([3,6,7,10,16,20,23,31,34,44,48,58,65,73,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[13,13,-8,13,13,-7,13,13,-9,-20,-10,13,13,-11,13,13,-14,-17,-18,13,13,13,13,13,13,-12,-13,-16,]),'IF':([3,6,7,10,16,20,23,31,34,44,48,58,65,73,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[14,14,-8,14,14,-7,14,14,-9,-20,-10,14,14,-11,14,14,-14,-17,-18,14,14,14,14,14,14,-12,-13,-16,]),'WRITE':([3,6,7,10,16,20,23,31,34,44,48,58,65,73,76,83,88,89,90,92,93,94,96,97,98,99,100,101,],[15,15,-8,15,15,-7,15,15,-9,-20,-10,15,15,-11,15,15,-14,-17,-18,15,15,15,15,15,15,-12,-13,-16,]),'COMMA':([4,5,32,85,95,],[17,-5,-3,-6,-4,]),'LEFT_BRACKET':([5,12,32,],[18,25,46,]),'END':([6,7,20,31,34,44,48,73,88,90,99,100,101,],[19,-8,-7,45,-9,-20,-10,-11,-14,-18,-12,-13,-16,]),'UNTIL':([7,20,23,34,44,48,73,88,90,99,100,101,],[-8,-7,37,-9,-20,-10,-11,-14,-18,-12,-13,-16,]),'ENDWHILE':([7,20,34,44,48,73,76,88,90,99,100,101,],[-8,-7,-9,-20,-10,-11,88,-14,-18,-12,-13,-16,]),'ELSE':([7,20,34,44,48,73,83,88,90,99,100,101,],[-8,-7,-9,-20,-10,-11,89,-14,-18,-12,-13,-16,]),'ENDIF':([7,20,34,44,48,73,83,88,90,98,99,100,101,],[-8,-7,-9,-20,-10,-11,90,-14,-18,101,-12,-13,-16,]),'ENDFOR':([7,20,34,44,48,73,88,90,96,97,99,100,101,],[-8,-7,-9,-20,-10,-11,-14,-18,99,100,-12,-13,-16,]),'ASSIGNMENT':([9,12,56,57,],[22,-35,-36,-37,]),'SEMICOLON':([12,21,28,29,30,35,36,54,56,57,68,69,70,71,72,77,78,79,80,81,82,],[-35,34,44,-33,-34,48,-21,73,-36,-37,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,]),'ADD':([12,29,30,36,56,57,],[-35,-33,-34,49,-36,-37,]),'SUB':([12,29,30,36,56,57,],[-35,-33,-34,50,-36,-37,]),'MUL':([12,29,30,36,56,57,],[-35,-33,-34,51,-36,-37,]),'DIV':([12,29,30,36,56,57,],[-35,-33,-34,52,-36,-37,]),'MOD':([12,29,30,36,56,57,],[-35,-33,-34,53,-36,-37,]),'EQUALS':([12,29,30,42,56,57,],[-35,-33,-34,59,-36,-37,]),'NOT_EQUALS':([12,29,30,42,56,57,],[-35,-33,-34,60,-36,-37,]),'LOWER':([12,29,30,42,56,57,],[-35,-33,-34,61,-36,-37,]),'GREATER':([12,29,30,42,56,57,],[-35,-33,-34,62,-36,-37,]),'LEQ':([12,29,30,42,56,57,],[-35,-33,-34,63,-36,-37,]),'GEQ':([12,29,30,42,56,57,],[-35,-33,-34,64,-36,-37,]),'TO':([12,29,30,55,56,57,],[-35,-33,-34,74,-36,-37,]),'DOWNTO':([12,29,30,55,56,57,],[-35,-33,-34,75,-36,-37,]),'DO':([12,29,30,41,56,57,77,78,79,80,81,82,86,87,],[-35,-33,-34,58,-36,-37,-27,-28,-29,-30,-31,-32,92,93,]),'THEN':([12,29,30,43,56,57,77,78,79,80,81,82,],[-35,-33,-34,65,-36,-37,-27,-28,-29,-30,-31,-32,]),'NUM':([13,14,15,18,22,25,26,27,37,38,46,47,49,50,51,52,53,59,60,61,62,63,64,74,75,84,],[-15,-19,29,33,29,40,29,29,29,29,66,67,29,29,29,29,29,29,29,29,29,29,29,29,29,91,]),'FROM':([24,],[38,]),'COLON':([33,66,],[47,84,]),'RIGHT_BRACKET':([39,40,67,91,],[56,57,85,95,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declarations':([2,],[4,]),'commands':([3,10,16,58,65,92,93,94,],[6,23,31,76,83,96,97,98,]),'command':([3,6,10,16,23,31,58,65,76,83,92,93,94,96,97,98,],[7,20,7,7,20,20,7,7,20,20,7,7,7,20,20,20,]),'identifier':([3,6,8,10,15,16,22,23,26,27,31,37,38,49,50,51,52,53,58,59,60,61,62,63,64,65,74,75,76,83,92,93,94,96,97,98,],[9,9,21,9,30,9,30,9,30,30,9,30,30,30,30,30,30,30,9,30,30,30,30,30,30,9,30,30,9,9,9,9,9,9,9,9,]),'while_occured':([13,],[26,]),'if_occured':([14,],[27,]),'value':([15,22,26,27,37,38,49,50,51,52,53,59,60,61,62,63,64,74,75,],[28,36,42,42,42,55,68,69,70,71,72,77,78,79,80,81,82,86,87,]),'expression':([22,],[35,]),'condition':([26,27,37,],[41,43,54,]),'else_occured':([89,],[94,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> DECLARE declarations BEGIN commands END','program',5,'p_program','code_parser.py',127),
  ('program -> BEGIN commands END','program',3,'p_program','code_parser.py',128),
  ('declarations -> declarations COMMA pidentifier','declarations',3,'p_declarations_muliple','code_parser.py',131),
  ('declarations -> declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET','declarations',8,'p_declarations_muliple','code_parser.py',132),
  ('declarations -> pidentifier','declarations',1,'p_declarations_single_var','code_parser.py',144),
  ('declarations -> pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET','declarations',6,'p_declarations_single_tab','code_parser.py',154),
  ('commands -> commands command','commands',2,'p_commands','code_parser.py',168),
  ('commands -> command','commands',1,'p_commands','code_parser.py',169),
  ('command -> READ identifier SEMICOLON','command',3,'p_command_read','code_parser.py',172),
  ('command -> identifier ASSIGNMENT expression SEMICOLON','command',4,'p_command_assignment','code_parser.py',200),
  ('command -> REPEAT commands UNTIL condition SEMICOLON','command',5,'p_command_all','code_parser.py',527),
  ('command -> FOR pidentifier FROM value TO value DO commands ENDFOR','command',9,'p_command_all','code_parser.py',528),
  ('command -> FOR pidentifier FROM value DOWNTO value DO commands ENDFOR','command',9,'p_command_all','code_parser.py',529),
  ('command -> WHILE while_occured condition DO commands ENDWHILE','command',6,'p_command_while','code_parser.py',532),
  ('while_occured -> <empty>','while_occured',0,'p_command_while_occured','code_parser.py',539),
  ('command -> IF if_occured condition THEN commands ELSE else_occured commands ENDIF','command',9,'p_command_if_else','code_parser.py',548),
  ('else_occured -> <empty>','else_occured',0,'p_command_else_occured','code_parser.py',562),
  ('command -> IF if_occured condition THEN commands ENDIF','command',6,'p_command_if_endif','code_parser.py',575),
  ('if_occured -> <empty>','if_occured',0,'p_if_occured','code_parser.py',589),
  ('command -> WRITE value SEMICOLON','command',3,'p_command_write','code_parser.py',595),
  ('expression -> value','expression',1,'p_expression_val','code_parser.py',632),
  ('expression -> value ADD value','expression',3,'p_expression_math','code_parser.py',636),
  ('expression -> value SUB value','expression',3,'p_expression_math','code_parser.py',637),
  ('expression -> value MUL value','expression',3,'p_expression_math','code_parser.py',638),
  ('expression -> value DIV value','expression',3,'p_expression_math','code_parser.py',639),
  ('expression -> value MOD value','expression',3,'p_expression_math','code_parser.py',640),
  ('condition -> value EQUALS value','condition',3,'p_condition','code_parser.py',725),
  ('condition -> value NOT_EQUALS value','condition',3,'p_condition','code_parser.py',726),
  ('condition -> value LOWER value','condition',3,'p_condition','code_parser.py',727),
  ('condition -> value GREATER value','condition',3,'p_condition','code_parser.py',728),
  ('condition -> value LEQ value','condition',3,'p_condition','code_parser.py',729),
  ('condition -> value GEQ value','condition',3,'p_condition','code_parser.py',730),
  ('value -> NUM','value',1,'p_value_num','code_parser.py',989),
  ('value -> identifier','value',1,'p_value_identifier','code_parser.py',993),
  ('identifier -> pidentifier','identifier',1,'p_identifier','code_parser.py',997),
  ('identifier -> pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET','identifier',4,'p_identifier','code_parser.py',998),
  ('identifier -> pidentifier LEFT_BRACKET NUM RIGHT_BRACKET','identifier',4,'p_identifier_tab','code_parser.py',1010),
]
