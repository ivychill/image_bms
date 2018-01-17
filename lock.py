#-*-coding:utf-8-*-
import lock_l1,lock_l2,lock_l3,lock_l4,lock_l5
import enum

if __name__=="__main__":

 r1=lock_l1.match_t1('./lock.jpg','./l1.jpg','0.99')
 # a=r1[1]
 r2=lock_l2.match_t2('./lock.jpg','./l2.jpg','0.99')
 # b=r2[1]
 r3=lock_l3.match_t3('./lock.jpg','./l3.jpg','0.99')
 # c=r3[1]
 r4=lock_l4.match_t4('./lock.jpg','./l4.jpg','0.99')
 # d=r4[1]
 r5=lock_l5.match_t5('./lock.jpg','./l5.jpg','0.99')
 # e=r5[1]

# print a>b
# print a>c
# print a>d
# print a>e
#  f=[a,b,c,d,e]
#  f.sort()
#  print f


class region(enum.IntEnum):
    a = r1[1]
    b = r2[1]
    c = r3[1]
    d = r4[1]
    e = r5[1]
try:
    print('\n'.join(s.name for s in sorted(region)))
except TypeError as err:
    print('Error : {}'.format(err))




