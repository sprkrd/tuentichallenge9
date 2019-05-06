
(define (problem test-problem)
(:domain character-6)
(:objects char0 char1 char2 - character s0 s1 s2 - skill)
(:init
  (empty-slot slot0)
  (empty-slot slot1)
  (HAS-SKILL char0 s0)
  (HAS-SKILL char0 s1)
  (HAS-SKILL char1 s1)
  (HAS-:SKILL char2 s1)
  (HAS-SKILL char2 s2)
  (CAN-BE-FUSED-INTO char0 char1 char2)
  (= (total-cost) 0)
  (= (cost char0) 200)
  (= (cost char1) 100)
  (= (cost char2) 2000)
)
(:goal (and (assigned-skill slot0 s2) (assigned-skill slot1 s1)))
(:metric minimize (total-cost))
)

