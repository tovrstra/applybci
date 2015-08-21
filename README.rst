Introduction
============

This is a simple script that detects bonds, assigns atom types and computes charges from
bond-increment parameters. This script assumes that Yaff and MolMod are installed. More
information about these packages can be found here:

* MolMod: http://molmod.github.io/molmod/
* Yaff: http://molmod.github.io/yaff/


Usage
=====

Using the example input files included in the git repository,
the script is executed as follows:

.. code-block:: bash

    ./applybci.py SAPO-34_1Si_O1.xyz rules.txt parameters.txt

You should get the following output

.. code-block:: text

    Detected 9 real numbers in title line.
    Treating system as periodic with the following cell vectors
    in Angstrom. (Cell vectors are displayed as rows.)
    [[ 13.80514326   0.           0.        ]
     [ -6.902524    11.95554191   0.        ]
     [  0.           0.          15.14906498]]

    Reading atom type rules
        H           1
        O_AlSi      8&=2&=1%13&=1%14
        O_AlSiH     8&=3&=1%13&=1%14&=1%1
        O_AlP       8&=2&=1%13&=1%15
        O_SiSi      8&=2&=2%14
        Al          13
        Si          14
        P           15

    Bond and atom type statistics
        Number of atoms:            111
        Number of bonds (12 pairs): 147
        Number of 13 pairs:         294
        Number of atoms by type
            H               3
            O_AlSi          9
            O_AlP          60
            O_AlSiH         3
            Al             18
            Si              3
            P              15
        Number of bonds (12 pairs) by type
            H           O_AlSiH         3
            O_AlSi      Al              9
            O_AlSi      Si              9
            O_AlP       Al             60
            O_AlP       P              60
            O_AlSiH     Al              3
            O_AlSiH     Si              3
        Number of 13 pairs by type
            H           Al              3
            H           Si              3
            O_AlSi      O_AlSi          9
            O_AlSi      O_AlP          27
            O_AlSi      O_AlSiH         9
            O_AlP       O_AlP         162
            O_AlP       O_AlSiH         9
            Al          Si             12
            Al          P              60

    Reading parameters
        BCI-12   Al          O_AlSi          0.2333
        BCI-12   Al          O_AlSiH         0.5103
        BCI-12   Al          O_AlP           0.2376
        BCI-12   Si          O_AlSi          0.1277
        BCI-12   Si          O_AlSiH         0.6907
        BCI-12   Si          O_SiSi          0.2736
        BCI-12   P           O_AlP           0.1701
        BCI-12   H           O_AlSiH         0.4229
        BCI-13   O_AlSi      O_AlSiH        -0.2434
        BCI-13   O_AlP       O_AlSiH        -0.0606
        BCI-13   O_SiSi      O_AlSiH        -0.0412

    Computing charges
        Setting charges according to CHARGE keywords
            Total charge: 0.0000000000e+00
        Adding 12 increments
            Total charge: 6.6613381478e-16
        Adding 13 increments
            Total charge: 6.6613381478e-16

    Atom types, coordinates (in Angstrom) and charges (in electron)
                 H     -2.3663      4.3233      0.0755      0.4229
            O_AlSi      4.9527      2.5242      6.9128     -0.6044
             O_AlP      0.2460      5.0522      6.9598     -0.4077
            O_AlSi      4.3307      0.0469      7.6350     -0.6044
             O_AlP     -7.8135     11.8231     14.9886     -0.4077
             O_AlP     -2.1563      6.4179     12.0683     -0.4077
            O_AlSi     -6.6641      8.9934     11.6396     -0.6044
             O_AlP     -2.6060      4.0456     12.5604     -0.4683
             O_AlP      5.9793      4.1490      4.8158     -0.4077
             O_AlP     -9.0594     10.4937      2.0217     -0.4077
             O_AlP      7.0612      1.0952      1.7747     -0.4077
             O_AlP     -9.5010      8.1239      2.5301     -0.4077
             O_AlP     -0.9383      8.0234     10.0533     -0.4077
             O_AlP     -7.0923      9.5423      8.2489     -0.4683
             O_AlP     -2.3818      6.8940      8.3345     -0.4077
             O_AlP     -6.4823     11.8221      7.5317     -0.4077
             O_AlP      5.5405     -0.0342      0.1211     -0.4077
             O_AlP      6.8101      1.3801     13.1413     -0.4077
             O_AlP     -9.5072     10.9208     13.3589     -0.4077
             O_AlP      7.3078      3.6998     12.4983     -0.4077
             O_AlP     -1.2288      3.9728      5.2440     -0.4077
             O_AlP     -0.1810      5.5607      3.1382     -0.4077
             O_AlP      4.3030      2.9434      3.3895     -0.4683
             O_AlP      0.2204      7.9572      2.6722     -0.4077
           O_AlSiH     -8.4981      7.8685     10.1539     -0.7119
                Al      0.7296      6.6995      6.6668      0.9504
                Al     -6.2113     10.6477     11.5932      0.9461
                Al     -6.2945      2.7650      1.4661      0.9461
                Al     -2.9338      5.2627      8.5479      0.9504
                Al      3.8564      9.2441     13.6489      0.9461
                Al      3.8610      1.2794      3.4538      1.2231
                Si     -7.7725      7.8635     11.7711      1.0738
                 P     -1.3634      8.0073      8.5806      0.6804
                 P     -8.3589     11.9148     13.5633      0.6804
                 P      5.3677      4.0580      3.4191      0.6804
                 P     -0.7897      3.9459      6.7050      0.6804
                 P      6.0263     -0.0050      1.5671      0.6804
                 H     -2.5609     -4.2109     10.1750      0.4229
            O_AlSi     -4.6624      3.0271     17.0122     -0.6044
             O_AlP     -4.4983     -2.3131     17.0593     -0.4077
            O_AlSi     -2.2059      3.7270     17.7344     -0.6044
             O_AlP     -6.3324    -12.6783     25.0880     -0.4077
             O_AlP     -4.4799     -5.0764     22.1677     -0.4077
            O_AlSi     -4.4565    -10.2680     21.7391     -0.6044
             O_AlP     -2.2006     -4.2797     22.6598     -0.4683
             O_AlP     -6.5828      3.1037     14.9153     -0.4077
             O_AlP     -4.5581    -13.0925     12.1211     -0.4077
             O_AlP     -4.4791      5.5675     11.8742     -0.4077
             O_AlP     -2.2851    -12.2900     12.6295     -0.4077
             O_AlP     -6.4793     -4.8243     20.1528     -0.4077
             O_AlP     -4.7177    -10.9132     18.3483     -0.4683
             O_AlP     -4.7795     -5.5097     18.4339     -0.4077
             O_AlP     -6.9971    -11.5249     17.6311     -0.4077
             O_AlP     -2.7407      4.8153     10.2206     -0.4077
             O_AlP     -4.6002      5.2076     23.2408     -0.4077
             O_AlP     -4.7040    -13.6939     23.4583     -0.4077
             O_AlP     -6.8580      4.4788     22.5977     -0.4077
             O_AlP     -2.8261     -3.0505     15.3435     -0.4077
             O_AlP     -4.7251     -2.9371     13.2376     -0.4077
             O_AlP     -4.7006      2.2548     13.4890     -0.4683
             O_AlP     -7.0014     -3.7877     12.7716     -0.4077
           O_AlSiH     -2.5652    -11.2938     20.2534     -0.7119
                Al     -6.1668     -2.7179     16.7662      0.9504
                Al     -6.1156    -10.7030     21.6926      0.9461
                Al      0.7527     -6.8337     11.5655      0.9461
                Al     -3.0907     -5.1721     18.6473      0.9504
                Al     -9.9338     -1.2823     23.7484      0.9461
                Al     -3.0385      2.7041     13.5532      1.2231
                Si     -2.9237    -10.6629     21.8706      1.0738
                 P     -6.2528     -5.1844     18.6800      0.6804
                 P     -6.1390    -13.1964     23.6628      0.6804
                 P     -6.1982      2.6196     13.5185      0.6804
                 P     -3.0223     -2.6569     16.8044      0.6804
                 P     -3.0088      5.2215     11.6665      0.6804
                 H      4.9272     -0.1124      5.1252      0.4229
            O_AlSi     -0.2904     -5.5513     11.9625     -0.6044
             O_AlP      4.2523     -2.7391     12.0095     -0.4077
            O_AlSi     -2.1247     -3.7739     12.6847     -0.6044
             O_AlP     14.1459      0.8551     20.0383     -0.4077
             O_AlP      6.6362     -1.3415     17.1180     -0.4077
            O_AlSi     11.1206      1.2746     16.6894     -0.6044
             O_AlP      4.8066      0.2341     17.6101     -0.4683
             O_AlP      0.6035     -7.2527      9.8655     -0.4077
             O_AlP     13.6175      2.5988      7.0714     -0.4077
             O_AlP     -2.5821     -6.6628      6.8245     -0.4077
             O_AlP     11.7860      4.1661      7.5798     -0.4077
             O_AlP      7.4176     -3.1991     15.1031     -0.4077
             O_AlP     11.8100      1.3709     13.2986     -0.4683
             O_AlP      7.1613     -1.3844     13.3842     -0.4077
             O_AlP     13.4794     -0.2972     12.5814     -0.4077
             O_AlP     -2.7999     -4.7812      5.1708     -0.4077
             O_AlP     -2.2098     -6.5877     18.1910     -0.4077
             O_AlP     14.2113      2.7731     18.4086     -0.4077
             O_AlP     -0.4497     -8.1786     17.5480     -0.4077
             O_AlP      4.0549     -0.9222     10.2937     -0.4077
             O_AlP      4.9062     -2.6235      8.1879     -0.4077
             O_AlP      0.3976     -5.1982      8.4393     -0.4683
             O_AlP      6.7810     -4.1695      7.7219     -0.4077
           O_AlSiH     11.0633      3.4253     15.2037     -0.7119
                Al      5.4372     -3.9817     11.7165      0.9504
                Al     12.3269      0.0553     16.6429      0.9461
                Al      5.5418      4.0687      6.5158      0.9461
                Al      6.0245     -0.0906     13.5976      0.9504
                Al      6.0775     -7.9618     18.6987      0.9461
                Al     -0.8225     -3.9835      8.5035      1.2231
                Si     10.6962      2.7994     16.8208      1.0738
                 P      7.6162     -2.8229     13.6303      0.6804
                 P     14.4980      1.2817     18.6131      0.6804
                 P      0.8305     -6.6775      8.4688      0.6804
                 P      3.8121     -1.2890     11.7547      0.6804
                 P     -3.0175     -5.2164      6.6168      0.6804

For more information on the file formats and command-line arguments, run the script with
the ``-h`` option.
