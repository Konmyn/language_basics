public class Pyramid {
    public static void main (String []args) {
        int layer = 10;
        for (int i=1; i<=layer; i++) {
            for (int k=layer-i; k>0; k--) {
                System.out.print(' ');
            }
            for (int j=1; j<=2*(i-1)+1; j++) {
                if (i==1 || i==layer){
                    System.out.print('*');
                } else {
                    if (j==1 || j==2*(i-1)+1) {
                        System.out.print('*');
                    } else {
                        System.out.print(' ');
                    }
                }

            }
            System.out.println("");
        }
    }
}