
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'normal_elASSIGN BG_CLOSE_EL BG_OPEN_EL COMMA COMMENT END_EL EV_FLAG EXE_FLAG FOR ID IF IN LPAR NAMESPACE_FLAG NORMSTRING NUMBER PIPE PUNCT QUOTE_1 QUOTE_2 RPARempty :attrs : attrs attr \n             | attr \n             | empty \n        fn : id LPAR expr RPAR\n           | id LPAR RPAR\n    \n        binop_expr : expr PIPE expr\n    \n        expr : id \n             | fn\n             | binop_expr\n    \n        assign_statement : id ASSIGN expr\n    \n        statement : assign_statement \n                  | expr\n    static_attr : tag_name ASSIGN QUOTE_1 NUMBER QUOTE_1\n           | tag_name ASSIGN QUOTE_2 NUMBER QUOTE_2\n           | tag_name ASSIGN NORMSTRING\n    \n        tag_name : ID\n                | tag_name NAMESPACE_FLAG ID\n    exec_attr : EXE_FLAG tag_name ASSIGN QUOTE_1 expr QUOTE_1\n           | EXE_FLAG tag_name ASSIGN QUOTE_2 expr QUOTE_2\n    event_attr : EV_FLAG ID ASSIGN QUOTE_1 statement QUOTE_1\n           | EV_FLAG ID ASSIGN QUOTE_2 statement QUOTE_2\n    attr : static_attr\n           | exec_attr\n           | event_attr\n    \n        id : id PUNCT ID\n            | ID\n    \n        end_el : BG_CLOSE_EL ID END_EL\n    op_el : BG_OPEN_EL ID attrs END_EL\n    \n        for_el : BG_OPEN_EL FOR ID IN id END_EL els BG_CLOSE_EL FOR END_EL\n    \n        if_el : BG_OPEN_EL IF expr END_EL els BG_CLOSE_EL IF END_EL\n    \n       normal_el : op_el els end_el \n    \n        els : els el\n            | el\n            | empty\n    el : normal_el\n          | for_el \n          | if_el\n    '
    
_lr_action_items = {'BG_OPEN_EL':([0,2,4,5,6,7,8,9,12,13,34,40,42,53,64,76,84,87,],[3,10,10,-34,-35,-36,-37,-38,-32,-33,-29,-28,10,10,10,10,-31,-30,]),'$end':([1,12,40,],[0,-32,-28,]),'BG_CLOSE_EL':([2,4,5,6,7,8,9,12,13,34,40,42,53,64,76,84,87,],[-1,14,-34,-35,-36,-37,-38,-32,-33,-29,-28,-1,65,-1,83,-31,-30,]),'ID':([3,10,11,14,15,16,18,19,20,21,22,23,25,26,35,37,41,43,44,45,48,60,61,62,63,67,68,78,79,80,81,82,],[11,11,17,27,28,33,17,-3,-4,-23,-24,-25,17,39,-2,49,33,33,55,33,-16,33,33,33,33,-14,-15,-19,-20,-21,33,-22,]),'FOR':([10,83,],[15,86,]),'IF':([10,65,],[16,77,]),'END_EL':([11,18,19,20,21,22,23,27,29,30,31,32,33,35,48,52,54,55,57,66,67,68,77,78,79,80,82,86,],[-1,34,-3,-4,-23,-24,-25,40,42,-8,-9,-10,-27,-2,-16,64,-7,-26,-6,-5,-14,-15,84,-19,-20,-21,-22,87,]),'EXE_FLAG':([11,18,19,20,21,22,23,35,48,67,68,78,79,80,82,],[25,25,-3,-4,-23,-24,-25,-2,-16,-14,-15,-19,-20,-21,-22,]),'EV_FLAG':([11,18,19,20,21,22,23,35,48,67,68,78,79,80,82,],[26,26,-3,-4,-23,-24,-25,-2,-16,-14,-15,-19,-20,-21,-22,]),'ASSIGN':([17,24,33,38,39,49,55,74,],[-17,36,-27,50,51,-18,-26,81,]),'NAMESPACE_FLAG':([17,24,38,49,],[-17,37,37,-18,]),'IN':([28,],[41,]),'PIPE':([29,30,31,32,33,54,55,56,57,66,69,70,73,74,85,],[43,-8,-9,-10,-27,43,-26,43,-6,-5,43,43,43,-8,43,]),'RPAR':([30,31,32,33,45,54,55,56,57,66,],[-8,-9,-10,-27,57,-7,-26,66,-6,-5,]),'QUOTE_1':([30,31,32,33,36,50,51,54,55,57,58,66,69,71,72,73,74,85,],[-8,-9,-10,-27,46,60,62,-7,-26,-6,67,-5,78,80,-12,-13,-8,-11,]),'QUOTE_2':([30,31,32,33,36,50,51,54,55,57,59,66,70,72,73,74,75,85,],[-8,-9,-10,-27,47,61,63,-7,-26,-6,68,-5,79,-12,-13,-8,82,-11,]),'PUNCT':([30,33,52,55,74,],[44,-27,44,-26,44,]),'LPAR':([30,33,55,74,],[45,-27,-26,45,]),'NORMSTRING':([36,],[48,]),'NUMBER':([46,47,],[58,59,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'normal_el':([0,2,4,42,53,64,76,],[1,7,7,7,7,7,7,]),'op_el':([0,2,4,42,53,64,76,],[2,2,2,2,2,2,2,]),'els':([2,42,64,],[4,53,76,]),'el':([2,4,42,53,64,76,],[5,13,5,13,5,13,]),'empty':([2,11,42,64,],[6,20,6,6,]),'for_el':([2,4,42,53,64,76,],[8,8,8,8,8,8,]),'if_el':([2,4,42,53,64,76,],[9,9,9,9,9,9,]),'end_el':([4,],[12,]),'attrs':([11,],[18,]),'attr':([11,18,],[19,35,]),'static_attr':([11,18,],[21,21,]),'exec_attr':([11,18,],[22,22,]),'event_attr':([11,18,],[23,23,]),'tag_name':([11,18,25,],[24,24,38,]),'expr':([16,43,45,60,61,62,63,81,],[29,54,56,69,70,73,73,85,]),'id':([16,41,43,45,60,61,62,63,81,],[30,52,30,30,30,30,74,74,30,]),'fn':([16,43,45,60,61,62,63,81,],[31,31,31,31,31,31,31,31,]),'binop_expr':([16,43,45,60,61,62,63,81,],[32,32,32,32,32,32,32,32,]),'statement':([62,63,],[71,75,]),'assign_statement':([62,63,],[72,72,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> normal_el","S'",1,None,None,None),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',4),
  ('attrs -> attrs attr','attrs',2,'p_attrs','parser.py',8),
  ('attrs -> attr','attrs',1,'p_attrs','parser.py',9),
  ('attrs -> empty','attrs',1,'p_attrs','parser.py',10),
  ('fn -> id LPAR expr RPAR','fn',4,'p_fn','parser.py',19),
  ('fn -> id LPAR RPAR','fn',3,'p_fn','parser.py',20),
  ('binop_expr -> expr PIPE expr','binop_expr',3,'p_binop_expr','parser.py',29),
  ('expr -> id','expr',1,'p_expr','parser.py',35),
  ('expr -> fn','expr',1,'p_expr','parser.py',36),
  ('expr -> binop_expr','expr',1,'p_expr','parser.py',37),
  ('assign_statement -> id ASSIGN expr','assign_statement',3,'p_assign_statement','parser.py',43),
  ('statement -> assign_statement','statement',1,'p_statement','parser.py',55),
  ('statement -> expr','statement',1,'p_statement','parser.py',56),
  ('static_attr -> tag_name ASSIGN QUOTE_1 NUMBER QUOTE_1','static_attr',5,'p_static_attr','parser.py',61),
  ('static_attr -> tag_name ASSIGN QUOTE_2 NUMBER QUOTE_2','static_attr',5,'p_static_attr','parser.py',62),
  ('static_attr -> tag_name ASSIGN NORMSTRING','static_attr',3,'p_static_attr','parser.py',63),
  ('tag_name -> ID','tag_name',1,'p_tag_name','parser.py',81),
  ('tag_name -> tag_name NAMESPACE_FLAG ID','tag_name',3,'p_tag_name','parser.py',82),
  ('exec_attr -> EXE_FLAG tag_name ASSIGN QUOTE_1 expr QUOTE_1','exec_attr',6,'p_exec_attr','parser.py',91),
  ('exec_attr -> EXE_FLAG tag_name ASSIGN QUOTE_2 expr QUOTE_2','exec_attr',6,'p_exec_attr','parser.py',92),
  ('event_attr -> EV_FLAG ID ASSIGN QUOTE_1 statement QUOTE_1','event_attr',6,'p_event_attr','parser.py',104),
  ('event_attr -> EV_FLAG ID ASSIGN QUOTE_2 statement QUOTE_2','event_attr',6,'p_event_attr','parser.py',105),
  ('attr -> static_attr','attr',1,'p_attr','parser.py',116),
  ('attr -> exec_attr','attr',1,'p_attr','parser.py',117),
  ('attr -> event_attr','attr',1,'p_attr','parser.py',118),
  ('id -> id PUNCT ID','id',3,'p_id','parser.py',124),
  ('id -> ID','id',1,'p_id','parser.py',125),
  ('end_el -> BG_CLOSE_EL ID END_EL','end_el',3,'p_end_el','parser.py',136),
  ('op_el -> BG_OPEN_EL ID attrs END_EL','op_el',4,'p_op_el','parser.py',141),
  ('for_el -> BG_OPEN_EL FOR ID IN id END_EL els BG_CLOSE_EL FOR END_EL','for_el',10,'p_for_el','parser.py',163),
  ('if_el -> BG_OPEN_EL IF expr END_EL els BG_CLOSE_EL IF END_EL','if_el',8,'p_if_el','parser.py',173),
  ('normal_el -> op_el els end_el','normal_el',3,'p_normal_el','parser.py',182),
  ('els -> els el','els',2,'p_els','parser.py',192),
  ('els -> el','els',1,'p_els','parser.py',193),
  ('els -> empty','els',1,'p_els','parser.py',194),
  ('el -> normal_el','el',1,'p_el','parser.py',202),
  ('el -> for_el','el',1,'p_el','parser.py',203),
  ('el -> if_el','el',1,'p_el','parser.py',204),
]
