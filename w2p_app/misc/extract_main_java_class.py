#!/usr/bin/env python
#https://stackoverflow.com/questions/33420424/extracting-java-main-class-name-in-python

import javalang # $ pip install javalang

java_source = """
import java.util.Scanner;
class sample{}
class second
{
    static boolean check_prime(int a)
    {
        int c=0;
        for (int i=1;i<=a; i++) {
            if(a%i==0)
                c++;
        }
        if(c == 2)
            return true;
        else
            return false;
    }
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter two numbers");
        int a = in.nextInt();
        int b = in.nextInt();
        if(check_prime(a) && check_prime(b))
        {
            if(b-a==2 || a-b==2)
                System.out.println("They are twin primes");
            else
                System.out.println("They are not twin primes");
        }
        else
            System.out.println("They might not be prime numbers");
    }
}
"""

java_source = '''
public class A {
     public static void ImDoingThisToMessYouUp () {
          String s = "public static void main (String[] args) {}";
     }
}

public class B {
      public static void main (String[] args) {}
}
'''


java_source = '''
public class Example{
 public static void main(String[] args){
  System.out.println("Print Statement 1");
 }
}
class JavaClass1{
 void method(){
  System.out.println("Print Statement 2");
 }
}
class JavaClass2{
 void method(){
  System.out.println("Print Statement 3");
 }
}
class JavaClass3{
 void method(){
  System.out.println("Print Statement 4");
 }
}
'''

java_source = '''/*  suma.java
    compile
        javac suma.java

    run
        java suma < test.in
*/
import java.util.Scanner;

public class suma {

    public static void main(String[] args) {

        // input
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();

        // sum
        int val, i, sum = 0;
        for (i=0; i<n; i++) {
            val = scan.nextInt();
            sum += val;
        }

        System.out.println(sum);
    }
}
'''
tree = javalang.parse.parse(java_source)
name = next(klass.name for klass in tree.types
            if isinstance(klass, javalang.tree.ClassDeclaration)
            for m in klass.methods
            if m.name == 'main' and m.modifiers.issuperset({'public', 'static'}))


print name