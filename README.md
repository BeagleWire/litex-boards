## Litex with GPMC access:

- Since We are writing the top verilog module manually the steps are bit higher, I will try to reduce it further in future.

- Generate the litex core as follows:
```
# In litex boards directory
$ ./litex_boards/targets/beaglewire.py --cpu-type=serv
```

- Copy the RTL to the gateware folder inside build
```
cd RTL
cp * ../build/beaglewire/gateware/
```

- open ``beaglewire.ys` file in `gateware` folder:

- Changes in `beaglewire.ys` file:
```
# Change on line 17:
read_verilog -I/<serv-address>/verilog/rtl /<beaglewire-dir>/build/beaglewire/gateware/beaglewire.v

#to 

read_verilog -I/<serv-address>/verilog/rtl /<beaglewire-dir>/build/beaglewire/gateware/top.v

#Change on line 20:
synth_ice40  -json beaglewire.json -top beaglewire -dsp

#to
synth_ice40  -json beaglewire.json -top top -dsp
```

- Building the core
```
cd beaglewire/gateware/
chmod +x build_beaglewire.sh
./build_beaglewire.sh
```

- Sending the file to the beaglewire
```
cd beaglewire/gateware/
cp beaglewire.bin beaglewire_bios.bin  &&  truncate beaglewire_bios.bin -s 4194304   && dd if=../software/bios/bios.bin of=beaglewire_bios.bin bs=1 seek=393216 conv=notrunc
scp beaglewire_bios.bin debian@192.168.6.2:/home/debian
```