
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programleftADDSUBleftMULDIVMODADD ASSIGNMENT BEGIN COLON COMMA DECLARE DIV DO DOWNTO ELSE END ENDFOR ENDIF ENDWHILE EQUALS FOR FROM GEQ GREATER IF LEFT_BRACKET LEQ LOWER MOD MUL NOT_EQUALS NUM READ REPEAT RIGHT_BRACKET SEMICOLON SUB THEN TO UNTIL WHILE WRITE pidentifierprogram : DECLARE declarations BEGIN commands END\n               | BEGIN commands ENDdeclarations : declarations COMMA pidentifier\n                    | declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKETdeclarations : pidentifierdeclarations : pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKETcommands : commands command\n                | commandcommand : READ identifier SEMICOLONcommand : identifier ASSIGNMENT expression SEMICOLONcommand : FOR  for_occured  pidentifier  FROM  value  DOWNTO  value DO do_occured commands  ENDFORcommand : FOR  for_occured  pidentifier  FROM  value TO  value DO do_occured commands  ENDFORdo_occured :for_occured :command : REPEAT repeat_occured  commands  UNTIL  condition SEMICOLONrepeat_occured :command : WHILE while_occured condition  DO  commands  ENDWHILEwhile_occured :command : IF if_occured condition THEN commands ELSE else_occured commands ENDIFelse_occured :command : IF if_occured condition  THEN  commands  ENDIFif_occured :command : WRITE value SEMICOLONexpression : valueexpression : value ADD value\n                  | value SUB value\n                  | value MUL value\n                  | value DIV value\n                  | value MOD valuecondition : value EQUALS value\n                 | value NOT_EQUALS value\n                 | value LOWER value\n                 | value GREATER value\n                 | value LEQ value\n                 | value GEQ valuevalue : NUMvalue : identifieridentifier : pidentifier\n                  | pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKETidentifier : pidentifier LEFT_BRACKET NUM RIGHT_BRACKET'
    
_lr_action_items = {'DECLARE':([0,],[2,]),'BEGIN':([0,4,5,32,84,95,],[3,16,-5,-3,-6,-4,]),'$end':([1,19,45,],[0,-2,-1,]),'pidentifier':([2,3,6,7,8,10,12,13,14,15,16,17,20,22,23,24,25,26,27,31,34,40,44,48,49,50,51,52,53,54,57,58,59,60,61,62,63,64,65,75,82,85,86,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[5,11,11,-8,11,-14,-16,-18,-22,11,11,32,-7,11,37,38,11,11,11,11,-9,11,-23,-10,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,-15,-17,-20,-21,11,-13,-13,11,11,11,-19,11,11,-11,-12,]),'READ':([3,6,7,12,16,20,25,31,34,40,44,48,58,65,75,82,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[8,8,-8,-16,8,-7,8,8,-9,8,-23,-10,8,8,8,8,-15,-17,-20,-21,8,-13,-13,8,8,8,-19,8,8,-11,-12,]),'FOR':([3,6,7,12,16,20,25,31,34,40,44,48,58,65,75,82,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[10,10,-8,-16,10,-7,10,10,-9,10,-23,-10,10,10,10,10,-15,-17,-20,-21,10,-13,-13,10,10,10,-19,10,10,-11,-12,]),'REPEAT':([3,6,7,12,16,20,25,31,34,40,44,48,58,65,75,82,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[12,12,-8,-16,12,-7,12,12,-9,12,-23,-10,12,12,12,12,-15,-17,-20,-21,12,-13,-13,12,12,12,-19,12,12,-11,-12,]),'WHILE':([3,6,7,12,16,20,25,31,34,40,44,48,58,65,75,82,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[13,13,-8,-16,13,-7,13,13,-9,13,-23,-10,13,13,13,13,-15,-17,-20,-21,13,-13,-13,13,13,13,-19,13,13,-11,-12,]),'IF':([3,6,7,12,16,20,25,31,34,40,44,48,58,65,75,82,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[14,14,-8,-16,14,-7,14,14,-9,14,-23,-10,14,14,14,14,-15,-17,-20,-21,14,-13,-13,14,14,14,-19,14,14,-11,-12,]),'WRITE':([3,6,7,12,16,20,25,31,34,40,44,48,58,65,75,82,87,88,89,90,94,96,97,98,99,100,101,102,103,104,105,],[15,15,-8,-16,15,-7,15,15,-9,15,-23,-10,15,15,15,15,-15,-17,-20,-21,15,-13,-13,15,15,15,-19,15,15,-11,-12,]),'COMMA':([4,5,32,84,95,],[17,-5,-3,-6,-4,]),'LEFT_BRACKET':([5,11,32,],[18,24,46,]),'END':([6,7,20,31,34,44,48,87,88,90,101,104,105,],[19,-8,-7,45,-9,-23,-10,-15,-17,-21,-19,-11,-12,]),'UNTIL':([7,20,34,40,44,48,87,88,90,101,104,105,],[-8,-7,-9,57,-23,-10,-15,-17,-21,-19,-11,-12,]),'ENDWHILE':([7,20,34,44,48,75,87,88,90,101,104,105,],[-8,-7,-9,-23,-10,88,-15,-17,-21,-19,-11,-12,]),'ELSE':([7,20,34,44,48,82,87,88,90,101,104,105,],[-8,-7,-9,-23,-10,89,-15,-17,-21,-19,-11,-12,]),'ENDIF':([7,20,34,44,48,82,87,88,90,98,101,104,105,],[-8,-7,-9,-23,-10,90,-15,-17,-21,101,-19,-11,-12,]),'ENDFOR':([7,20,34,44,48,87,88,90,101,102,103,104,105,],[-8,-7,-9,-23,-10,-15,-17,-21,-19,104,105,-11,-12,]),'ASSIGNMENT':([9,11,55,56,],[22,-38,-39,-40,]),'SEMICOLON':([11,21,28,29,30,35,36,55,56,68,69,70,71,72,74,76,77,78,79,80,81,],[-38,34,44,-36,-37,48,-24,-39,-40,-25,-26,-27,-28,-29,87,-30,-31,-32,-33,-34,-35,]),'ADD':([11,29,30,36,55,56,],[-38,-36,-37,49,-39,-40,]),'SUB':([11,29,30,36,55,56,],[-38,-36,-37,50,-39,-40,]),'MUL':([11,29,30,36,55,56,],[-38,-36,-37,51,-39,-40,]),'DIV':([11,29,30,36,55,56,],[-38,-36,-37,52,-39,-40,]),'MOD':([11,29,30,36,55,56,],[-38,-36,-37,53,-39,-40,]),'EQUALS':([11,29,30,42,55,56,],[-38,-36,-37,59,-39,-40,]),'NOT_EQUALS':([11,29,30,42,55,56,],[-38,-36,-37,60,-39,-40,]),'LOWER':([11,29,30,42,55,56,],[-38,-36,-37,61,-39,-40,]),'GREATER':([11,29,30,42,55,56,],[-38,-36,-37,62,-39,-40,]),'LEQ':([11,29,30,42,55,56,],[-38,-36,-37,63,-39,-40,]),'GEQ':([11,29,30,42,55,56,],[-38,-36,-37,64,-39,-40,]),'DOWNTO':([11,29,30,55,56,73,],[-38,-36,-37,-39,-40,85,]),'TO':([11,29,30,55,56,73,],[-38,-36,-37,-39,-40,86,]),'DO':([11,29,30,41,55,56,76,77,78,79,80,81,92,93,],[-38,-36,-37,58,-39,-40,-30,-31,-32,-33,-34,-35,96,97,]),'THEN':([11,29,30,43,55,56,76,77,78,79,80,81,],[-38,-36,-37,65,-39,-40,-30,-31,-32,-33,-34,-35,]),'NUM':([13,14,15,18,22,24,26,27,46,47,49,50,51,52,53,54,57,59,60,61,62,63,64,83,85,86,],[-18,-22,29,33,29,39,29,29,66,67,29,29,29,29,29,29,29,29,29,29,29,29,29,91,29,29,]),'COLON':([33,66,],[47,83,]),'FROM':([37,],[54,]),'RIGHT_BRACKET':([38,39,67,91,],[55,56,84,95,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declarations':([2,],[4,]),'commands':([3,16,25,58,65,94,99,100,],[6,31,40,75,82,98,102,103,]),'command':([3,6,16,25,31,40,58,65,75,82,94,98,99,100,102,103,],[7,20,7,7,20,20,7,7,20,20,7,20,7,7,20,20,]),'identifier':([3,6,8,15,16,22,25,26,27,31,40,49,50,51,52,53,54,57,58,59,60,61,62,63,64,65,75,82,85,86,94,98,99,100,102,103,],[9,9,21,30,9,30,9,30,30,9,9,30,30,30,30,30,30,30,9,30,30,30,30,30,30,9,9,9,30,30,9,9,9,9,9,9,]),'for_occured':([10,],[23,]),'repeat_occured':([12,],[25,]),'while_occured':([13,],[26,]),'if_occured':([14,],[27,]),'value':([15,22,26,27,49,50,51,52,53,54,57,59,60,61,62,63,64,85,86,],[28,36,42,42,68,69,70,71,72,73,42,76,77,78,79,80,81,92,93,]),'expression':([22,],[35,]),'condition':([26,27,57,],[41,43,74,]),'else_occured':([89,],[94,]),'do_occured':([96,97,],[99,100,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> DECLARE declarations BEGIN commands END','program',5,'p_program','code_parser.py',142),
  ('program -> BEGIN commands END','program',3,'p_program','code_parser.py',143),
  ('declarations -> declarations COMMA pidentifier','declarations',3,'p_declarations_muliple','code_parser.py',146),
  ('declarations -> declarations COMMA pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET','declarations',8,'p_declarations_muliple','code_parser.py',147),
  ('declarations -> pidentifier','declarations',1,'p_declarations_single_var','code_parser.py',159),
  ('declarations -> pidentifier LEFT_BRACKET NUM COLON NUM RIGHT_BRACKET','declarations',6,'p_declarations_single_tab','code_parser.py',169),
  ('commands -> commands command','commands',2,'p_commands','code_parser.py',183),
  ('commands -> command','commands',1,'p_commands','code_parser.py',184),
  ('command -> READ identifier SEMICOLON','command',3,'p_command_read','code_parser.py',187),
  ('command -> identifier ASSIGNMENT expression SEMICOLON','command',4,'p_command_assignment','code_parser.py',214),
  ('command -> FOR for_occured pidentifier FROM value DOWNTO value DO do_occured commands ENDFOR','command',11,'p_command_for_down_to','code_parser.py',559),
  ('command -> FOR for_occured pidentifier FROM value TO value DO do_occured commands ENDFOR','command',11,'p_command_for_from_to','code_parser.py',562),
  ('do_occured -> <empty>','do_occured',0,'p_cpmmand_do_occured','code_parser.py',572),
  ('for_occured -> <empty>','for_occured',0,'p_command_for_occured','code_parser.py',721),
  ('command -> REPEAT repeat_occured commands UNTIL condition SEMICOLON','command',6,'p_command_repeat_until','code_parser.py',729),
  ('repeat_occured -> <empty>','repeat_occured',0,'p_command_repeat_occured','code_parser.py',739),
  ('command -> WHILE while_occured condition DO commands ENDWHILE','command',6,'p_command_while','code_parser.py',748),
  ('while_occured -> <empty>','while_occured',0,'p_command_while_occured','code_parser.py',758),
  ('command -> IF if_occured condition THEN commands ELSE else_occured commands ENDIF','command',9,'p_command_if_else','code_parser.py',767),
  ('else_occured -> <empty>','else_occured',0,'p_command_else_occured','code_parser.py',781),
  ('command -> IF if_occured condition THEN commands ENDIF','command',6,'p_command_if_endif','code_parser.py',794),
  ('if_occured -> <empty>','if_occured',0,'p_if_occured','code_parser.py',808),
  ('command -> WRITE value SEMICOLON','command',3,'p_command_write','code_parser.py',814),
  ('expression -> value','expression',1,'p_expression_val','code_parser.py',851),
  ('expression -> value ADD value','expression',3,'p_expression_math','code_parser.py',855),
  ('expression -> value SUB value','expression',3,'p_expression_math','code_parser.py',856),
  ('expression -> value MUL value','expression',3,'p_expression_math','code_parser.py',857),
  ('expression -> value DIV value','expression',3,'p_expression_math','code_parser.py',858),
  ('expression -> value MOD value','expression',3,'p_expression_math','code_parser.py',859),
  ('condition -> value EQUALS value','condition',3,'p_condition','code_parser.py',954),
  ('condition -> value NOT_EQUALS value','condition',3,'p_condition','code_parser.py',955),
  ('condition -> value LOWER value','condition',3,'p_condition','code_parser.py',956),
  ('condition -> value GREATER value','condition',3,'p_condition','code_parser.py',957),
  ('condition -> value LEQ value','condition',3,'p_condition','code_parser.py',958),
  ('condition -> value GEQ value','condition',3,'p_condition','code_parser.py',959),
  ('value -> NUM','value',1,'p_value_num','code_parser.py',1270),
  ('value -> identifier','value',1,'p_value_identifier','code_parser.py',1274),
  ('identifier -> pidentifier','identifier',1,'p_identifier','code_parser.py',1278),
  ('identifier -> pidentifier LEFT_BRACKET pidentifier RIGHT_BRACKET','identifier',4,'p_identifier','code_parser.py',1279),
  ('identifier -> pidentifier LEFT_BRACKET NUM RIGHT_BRACKET','identifier',4,'p_identifier_tab','code_parser.py',1291),
]
