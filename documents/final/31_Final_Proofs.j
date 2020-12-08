CONJECTUREPANEL Conjectures
PROOF "S2∧HC3→(HC3∧HC4∧¬HD3)∨(HC3∧HD3∧¬HC4), ¬HC4→HD3, ¬HD3→HC4, HC3, S2 ⊢ (S2∧HC3∧(HC4∧¬HD3)∨(HD3∧¬HC4))"
INFER S2∧HC3→(HC3∧HC4∧¬HD3)∨(HC3∧HD3∧¬HC4),
     ¬HC4→HD3,
     ¬HD3→HC4,
     HC3,
     S2 
     ⊢ (S2∧HC3∧(HC4∧¬HD3)∨(HD3∧¬HC4))
FORMULAE
0 HD3∧¬HC4,
1 S2∧HC3∧(HC4∧¬HD3),
2 S2∧HC3∧(HC4∧¬HD3)∨(HD3∧¬HC4),
3 ¬HC4,
4 HD3,
5 HC3∧HD3,
6 HC3,
7 HC3∧HD3∧¬HC4,
8 HC4∧¬HD3,
9 S2∧HC3,
10 ¬HD3,
11 HC4,
12 ¬HD3→HC4,
13 HC3∧HC4∧¬HD3,
14 HC3∧HC4,
15 HC3∧HC4∧¬HD3∨HC3∧HD3∧¬HC4,
16 S2∧HC3→(HC3∧HC4∧¬HD3)∨(HC3∧HD3∧¬HC4),
17 (HC3∧HC4∧¬HD3)∨(HC3∧HD3∧¬HC4),
18 S2,
19 ¬HC4→HD3 
IS
SEQ (cut[B,C\9,2]) ("∧ intro"[A,B\18,6]) (hyp[A\18]) (hyp[A\6]) (cut[B,C\9,2]) (hyp[A\9]) (cut[B,C\17,2]) ("→ elim"[A,B\9,17]) (hyp[A\16]) (hyp[A\9]) ("∨ elim"[A,B,C\13,7,2]) (hyp[A\15]) (cut[B,C\10,2]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\14,10]) (hyp[A\13])) (cut[B,C\11,2]) ("→ elim"[A,B\10,11]) (hyp[A\12]) (hyp[A\10]) (cut[B,C\8,2]) ("∧ intro"[A,B\11,10]) (hyp[A\11]) (hyp[A\10]) (cut[B,C\8,2]) (hyp[A\8]) (cut[B,C\1,2]) ("∧ intro"[A,B\9,8]) (hyp[A\9]) (hyp[A\8]) (LAYOUT "∨ intro" (0) ("∨ intro(L)"[B,A\0,1]) (hyp[A\1])) (cut[B,C\3,2]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\5,3]) (hyp[A\7])) (cut[B,C\5,2]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\5,3]) (hyp[A\7])) (cut[B,C\4,2]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\6,4]) (hyp[A\5])) (cut[B,C\0,2]) ("∧ intro"[A,B\4,3]) (hyp[A\4]) (hyp[A\3]) (cut[B,C\0,2]) (hyp[A\0]) (LAYOUT "∨ intro" (0) ("∨ intro(R)"[B,A\1,0]) (hyp[A\0]))
END
CONJECTUREPANEL Conjectures
PROOF "(S2→S3), (S2∧S3∧¬S1), ¬S3 ⊢ S1"
INFER (S2→S3),
     (S2∧S3∧¬S1),
     ¬S3 
     ⊢ S1 
FORMULAE
0 ⊥,
1 S1,
2 ¬S2,
3 S2,
4 S2∧S3,
5 S3,
6 S2∧S3∧¬S1,
7 ¬S1,
8 ¬S3,
9 S2→S3 
IS
SEQ (cut[B,C\2,1]) ("→ MT"[A,B\3,5]) (hyp[A\9]) (hyp[A\8]) (cut[B,C\7,1]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\4,7]) (hyp[A\6])) (cut[B,C\4,1]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\4,7]) (hyp[A\6])) (cut[B,C\3,1]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\3,5]) (hyp[A\4])) (cut[B,C\0,1]) ("¬ elim"[B\3]) (hyp[A\3]) (hyp[A\2]) ("contra (constructive)"[B\1]) (hyp[A\0])
END
CONJECTUREPANEL Conjectures
PROOF "S4∧HC3∧HC4, S4∧HC3∧HC4→HC5, S5→HE4∧HE5 ⊢ (S4→HC3∧HC4∧HC5)∧(S5→HE4∧HE5)"
INFER S4∧HC3∧HC4,
     S4∧HC3∧HC4→HC5,
     S5→HE4∧HE5 
     ⊢ (S4→HC3∧HC4∧HC5)∧(S5→HE4∧HE5)
FORMULAE
0 S5→HE4∧HE5,
1 S4→HC3∧HC4∧HC5,
2 HC3∧HC4∧HC5,
3 S4,
4 (S4→HC3∧HC4∧HC5)∧(S5→HE4∧HE5),
5 HC5,
6 HC3∧HC4,
7 S4∧HC3∧HC4,
8 S4∧HC3∧HC4→HC5,
9 HC4,
10 HC3,
11 S4∧HC3 
IS
SEQ (cut[B,C\9,4]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\11,9]) (hyp[A\7])) (cut[B,C\11,4]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\11,9]) (hyp[A\7])) (cut[B,C\10,4]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\3,10]) (hyp[A\11])) (cut[B,C\6,4]) ("∧ intro"[A,B\10,9]) (hyp[A\10]) (hyp[A\9]) (cut[B,C\5,4]) ("→ elim"[A,B\7,5]) (hyp[A\8]) (hyp[A\7]) (cut[B,C\2,4]) ("∧ intro"[A,B\6,5]) (hyp[A\6]) (hyp[A\5]) (cut[B,C\1,4]) ("→ intro"[A,B\3,2]) (hyp[A\2]) ("∧ intro"[A,B\1,0]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Conjectures
PROOF "(PC1∧PD1∧PE1)→(PA1∧PA2), (PC1∧PD1∧PE1)∧(PA1∧PA2)∧¬(PA1∧PB1), ¬(PA1∧PA2) ⊢ (PA1∧PB1)"
INFER (PC1∧PD1∧PE1)→(PA1∧PA2),
     (PC1∧PD1∧PE1)∧(PA1∧PA2)∧¬(PA1∧PB1),
     ¬(PA1∧PA2)
     ⊢ (PA1∧PB1)
FORMULAE
0 ⊥,
1 PA1∧PB1,
2 ¬(PC1∧PD1∧PE1),
3 PC1∧PD1∧PE1,
4 ¬(PA1∧PA2),
5 PC1∧PD1∧PE1→PA1∧PA2,
6 PA1∧PA2,
7 (PC1∧PD1∧PE1)∧(PA1∧PA2)∧¬(PA1∧PB1),
8 (PC1∧PD1∧PE1)∧(PA1∧PA2),
9 ¬(PA1∧PB1),
10 PC1∧PD1∧PE1∧(PA1∧PA2),
11 ¬(PA1∧PA2),
12 (PC1∧PD1∧PE1)→(PA1∧PA2)
IS
SEQ (cut[B,C\8,1]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\8,9]) (hyp[A\7])) (cut[B,C\3,1]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\3,6]) (hyp[A\10])) (cut[B,C\9,1]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\8,9]) (hyp[A\7])) (cut[B,C\2,1]) ("→ MT"[A,B\3,6]) (hyp[A\5]) (hyp[A\4]) (cut[B,C\0,1]) ("¬ elim"[B\3]) (hyp[A\3]) (hyp[A\2]) ("contra (constructive)"[B\1]) (hyp[A\0])
END
