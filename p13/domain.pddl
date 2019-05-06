(define (domain character-6)
(:requirements :adl :typing :action-costs)
(:types character-slot character skill)
(:constants slot0 slot1 - character-slot)
(:predicates
  (contains-character ?charslot - character-slot ?char - character)
  (empty-slot ?charslot - character-slot)
  (assigned-skill ?charslot - character-slot ?s - skill)
  (HAS-SKILL ?char - character ?s - skill)
  (CAN-BE-FUSED-INTO ?char0 ?char1 ?result - character)
)
(:functions
  (total-cost)
  (cost ?char - character)
)
(:action buy-character
:parameters (?char - character ?charslot - character-slot)
:precondition (empty-slot ?charslot)
:effect (and
  (not (empty-slot ?charslot))
  (contains-character ?charslot ?char)
  (forall (?s - skill) (when (HAS-SKILL ?char ?s)
    (assigned-skill ?charslot ?s)))
  (increase (total-cost) (cost ?char))))
(:action fuse
:parameters (?char0 ?char1 ?result - character ?slot0 ?slot1 - character-slot)
:precondition (and
  (not (= ?slot0 ?slot1))
  (CAN-BE-FUSED-INTO ?char0 ?char1 ?result)
  (contains-character ?slot0 ?char0)
  (contains-character ?slot1 ?char1)
)
:effect (and
  (not (contains-character ?slot0 ?char0))
  (not (contains-character ?slot1 ?char1))
  (contains-character ?slot0 ?result)
  (empty-slot ?slot1)
  (forall (?s - skill) (when (HAS-SKILL ?result ?s)
    (assigned-skill ?slot0 ?s)))
  (forall (?s - skill) (when (assigned-skill ?slot1 ?s)
    (and
      (not (assigned-skill ?slot1 ?s))
      (assigned-skill ?slot0 ?s))))
))
)