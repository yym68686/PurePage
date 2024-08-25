# 一生一芯

环境：

- ubuntu 20.04

学习记录：[https://docs.qq.com/sheet/DS3V6SUtBak10TnFK](https://docs.qq.com/sheet/DS3V6SUtBak10TnFK)

预学习讲义：https://ysyx.oscc.cc/docs/prestudy/0.4.html

## 搭建 verilator 仿真环境

下载仓库：

```bash
git clone -b ysyx2204 https://github.com/OSCPU/ysyx-workbench.git
```

设置环境变量：

bashrc

```bash
echo "export NPC_HOME=/home/yanyuming/ysyx-workbench/npc" >> ~/.bashrc
source ~/.bashrc
```

zshrc

```bash
cat > ~/.zshrc << EOF
export NPC_HOME=/home/yym/ysyx-workbench/npc
EOF
source ~/.zshrc
```

一键安装 verilator

```bash
# Prerequisites:
sudo apt-get install -y git perl python3 make autoconf g++ flex bison ccache
sudo apt-get install -y libgoogle-perftools-dev numactl perl-doc
sudo apt-get install -y libfl2  # Ubuntu only (ignore if gives error)
sudo apt-get install -y libfl-dev  # Ubuntu only (ignore if gives error)
sudo apt-get install -y zlibc zlib1g zlib1g-dev  # Ubuntu only (ignore if gives error)

git clone https://github.com/verilator/verilator.git   # Only first time

# Every time you need to build:
unsetenv VERILATOR_ROOT  # For csh; ignore error if on bash
unset VERILATOR_ROOT  # For bash
cd verilator
git pull         # Make sure git repository is up-to-date
git tag          # See what versions exist
#git checkout master      # Use development branch (e.g. recent bug fixes)
#git checkout stable      # Use most recent stable release
git checkout v4.210  # Switch to specified release version

autoconf         # Create ./configure script
./configure      # Configure and create Makefile
make -j `nproc`  # Build Verilator itself (if error, try just 'make')
sudo make install
```

### verilator Hello World!

verilator 手册：[Verilator User’s Guide — Verilator 4.225 documentation](https://verilator.org/guide/latest/)

编写文件：

```bash
mkdir test_our
cd test_our

cat >our.v <<'EOF'
  module our;
     initial begin $display("Hello World"); $finish; end
  endmodule
EOF

cat >sim_main.cpp <<'EOF'
  #include "Vour.h"
  #include "verilated.h"
  int main(int argc, char** argv, char** env) {
      VerilatedContext* contextp = new VerilatedContext;
      contextp->commandArgs(argc, argv);
      Vour* top = new Vour{contextp};
      while (!contextp->gotFinish()) { top->eval(); }
      delete top;
      delete contextp;
      return 0;
  }
EOF
```

编译：

```bash
verilator -Wall --cc --exe --build sim_main.cpp our.v
```

各参数意义：

1. -Wall so Verilator has stronger lint warnings enabled.
2. --cc to get C++ output (versus e.g. SystemC or only linting).
3. `--exe`, along with our **sim_main.cpp** wrapper file, so the build will create an executable instead of only a library.
4. `--build`so Verilator will call make itself. This is we don’t need to manually call make as a separate step. You can also write your own compile rules, and run make yourself as we show in [Example SystemC Execution](https://verilator.org/guide/latest/example_sc.html#example-systemc-execution).)
5. An finally, **our.v** which is our SystemVerilog design file.

运行：

```bash
obj_dir/Vour
```

输出：

```bash
➜  test_our obj_dir/Vour
Hello World
- our.v:2: Verilog $finish
```

### 示例: 双控开关

top.v

```c
module top(
  input a,
  input b,
  output f
);
  assign f = a ^ b;
endmodule

```

最后一行需要有一行空行，否则编译报错。

main.cpp

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
 
#include "Vtop.h"  // create `top.v`,so use `Vtop.h`
#include "verilated.h"
 
#include "verilated_vcd_c.h" //可选，如果要导出vcd则需要加上
 
int main(int argc, char** argv, char** env) {
 
  VerilatedContext* contextp = new VerilatedContext;
  contextp->commandArgs(argc, argv);
  Vtop* top = new Vtop{contextp};
  
 
  VerilatedVcdC* tfp = new VerilatedVcdC; //初始化VCD对象指针
  contextp->traceEverOn(true); //打开追踪功能
  top->trace(tfp, 0); //
  tfp->open("wave.vcd"); //设置输出的文件wave.vcd
 
 
  while (!contextp->gotFinish()) {
    int a = rand() & 1;
    int b = rand() & 1;
    top->a = a;
    top->b = b;
    top->eval(); // eval()函数更新电路的状态, 这样我们就可以读取输出端口的值并打印
    printf("a = %d, b = %d, f = %d\n", a, b, top->f);
 
    tfp->dump(contextp->time()); //dump wave
    contextp->timeInc(1); //推动仿真时间
 
    assert(top->f == a ^ b); // 自动检查结果是否正确
  }
  delete top;
  tfp->close();
  delete contextp;
  return 0;
}
```

编译

```bash
verilator -Wall --cc --trace --exe --build top.v main.cpp
```

- --trace 是为了显示波形的

生成 vcd 波形文件

```bash
./obj_dir/Vtop
```

安装 gtkwave 查看波形

```bash
sudo apt-get -y install gtkwave
```

运行波形文件

```bash
gtkwave wave.vcd
```

### 编写 Makefile

Makefile

```makefile
all:
        @echo "Write this Makefile by your self."
sim:
        $(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
        @rm -rf obj_dir
        verilator -Wall --cc --trace --exe --build vsrc/top.v csrc/main.cpp

include ../Makefile
```

#### 一键仿真

```bash
make sim
```

### 接入 NVBoard

NVBoard 项目地址：[NJU-ProjectN/nvboard: NJU Virtual Board (github.com)](https://github.com/NJU-ProjectN/nvboard)

下载 NVBoard

```bash
cd ~/ysyx-workbench
bash init.sh nvboard
```

环境配置

```bash
apt-get install -y libsdl2-dev libsdl2-image-dev
echo 'export NVBOARD_HOME=/home/yym/ysyx-workbench/nvboard' >> ~/.zshrc
source ~/.zshrc
```

#### 运行 NVBoard 示例

```bash
cd nvboard/example
make run
```

看看 Makefile 内容

```makefile
TOPNAME = top
NXDC_FILES = constr/top.nxdc
INC_PATH ?=

VERILATOR = verilator
VERILATOR_CFLAGS += -MMD --build -cc  \
                                -O3 --x-assign fast --x-initial fast --noassert

BUILD_DIR = ./build
OBJ_DIR = $(BUILD_DIR)/obj_dir
BIN = $(BUILD_DIR)/$(TOPNAME)

default: $(BIN)

$(shell mkdir -p $(BUILD_DIR))

# constraint file
SRC_AUTO_BIND = $(abspath $(BUILD_DIR)/auto_bind.cpp)
$(SRC_AUTO_BIND): $(NXDC_FILES)
	python3 $(NVBOARD_HOME)/scripts/auto_pin_bind.py $^ $@

# project source
VSRCS = $(shell find $(abspath ./vsrc) -name "*.v")
CSRCS = $(shell find $(abspath ./csrc) -name "*.c" -or -name "*.cc" -or -name "*.cpp")
CSRCS += $(SRC_AUTO_BIND)

# rules for NVBoard
include $(NVBOARD_HOME)/scripts/nvboard.mk

# rules for verilator
INCFLAGS = $(addprefix -I, $(INC_PATH))
CFLAGS += $(INCFLAGS) -DTOP_NAME="\"V$(TOPNAME)\""
LDFLAGS += -lSDL2 -lSDL2_image

$(BIN): $(VSRCS) $(CSRCS) $(NVBOARD_ARCHIVE)
	@rm -rf $(OBJ_DIR)
	$(VERILATOR) $(VERILATOR_CFLAGS) \
                --top-module $(TOPNAME) $^ \
                $(addprefix -CFLAGS , $(CFLAGS)) $(addprefix -LDFLAGS , $(LDFLAGS)) \
                --Mdir $(OBJ_DIR) --exe -o $(abspath $(BIN))

all: default

run: $(BIN)
	@$^

clean:
	rm -rf $(BUILD_DIR)

.PHONY: default all clean run
```

#### 在 NVBoard 上实现双控开关

light.v

```c
module light(
  input clk,
  input rst,
  output reg [15:0] led
);
  reg [31:0] count;
  always @(posedge clk) begin
    if (rst) begin led <= 1; count <= 0; end
    else begin
      if (count == 0) led <= {led[14:0], led[15]};
      count <= (count >= 5000000 ? 32'b0 : count + 1);
    end
  end
endmodule
```

main.c

```c
#include <nvboard.h>
#include <Vtop.h>

static TOP_NAME dut;

void nvboard_bind_all_pins(Vtop* top);

static void single_cycle() {
  dut.clk = 0; dut.eval();
  dut.clk = 1; dut.eval();
}

static void reset(int n) {
  dut.rst = 1;
  while (n -- > 0) single_cycle();
  dut.rst = 0;
}

int main() {
  nvboard_bind_all_pins(&dut);
  nvboard_init();

  reset(10);

  while(1) {
    nvboard_update();
    single_cycle();
  }
}
```

### 示例: 流水灯

Makefile

```makefile
TOPNAME = top
NXDC_FILES = constr/top.nxdc
INC_PATH ?=

VERILATOR = verilator
VERILATOR_CFLAGS += -MMD --build -cc  \
                                -O3 --x-assign fast --x-initial fast --noassert

BUILD_DIR = ./build
OBJ_DIR = $(BUILD_DIR)/obj_dir
BIN = $(BUILD_DIR)/$(TOPNAME)

default: $(BIN)

$(shell mkdir -p $(BUILD_DIR))

# constraint file
SRC_AUTO_BIND = $(abspath $(BUILD_DIR)/auto_bind.cpp)
$(SRC_AUTO_BIND): $(NXDC_FILES)
	python3 $(NVBOARD_HOME)/scripts/auto_pin_bind.py $^ $@

# project source
VSRCS = $(shell find $(abspath ./vsrc) -name "*.v")
CSRCS = $(shell find $(abspath ./csrc) -name "*.c" -or -name "*.cc" -or -name "*.cpp")
CSRCS += $(SRC_AUTO_BIND)

# rules for NVBoard
include $(NVBOARD_HOME)/scripts/nvboard.mk

# rules for verilator
INCFLAGS = $(addprefix -I, $(INC_PATH))
CFLAGS += $(INCFLAGS) -DTOP_NAME="\"V$(TOPNAME)\""
LDFLAGS += -lSDL2 -lSDL2_image

$(BIN): $(VSRCS) $(CSRCS) $(NVBOARD_ARCHIVE)
	@rm -rf $(OBJ_DIR)
	$(VERILATOR) $(VERILATOR_CFLAGS) \
                --top-module $(TOPNAME) $^ \
                $(addprefix -CFLAGS , $(CFLAGS)) $(addprefix -LDFLAGS , $(LDFLAGS)) \
                --Mdir $(OBJ_DIR) --exe -o $(abspath $(BIN))

all: default

run: $(BIN)
	@$^

clean:
	rm -rf $(BUILD_DIR)

.PHONY: default all clean run

```

- .PHONY作用：make  x表示执行x这个指定的命令，而不是要生成x文件。

top.v

```c
module top(
  input clk,
  input rst,
  output reg [15:0] led
);
  reg [31:0] count;
  always @(posedge clk) begin
    if (rst) begin led <= 1; count <= 0; end
    else begin
      if (count == 0) led <= {led[14:0], led[15]};
      count <= (count >= 5000000 ? 32'b0 : count + 1);
    end
  end
endmodule
```

main.c

```c
#include <nvboard.h>
#include <Vtop.h>

static TOP_NAME dut;

void nvboard_bind_all_pins(Vtop* top);

static void single_cycle() {
  dut.clk = 0; dut.eval();
  dut.clk = 1; dut.eval();
}

static void reset(int n) {
  dut.rst = 1;
  while (n -- > 0) single_cycle();
  dut.rst = 0;
}

int main() {
  nvboard_bind_all_pins(&dut);
  nvboard_init();

  reset(10);

  while(1) {
    nvboard_update();
    single_cycle();
  }
}
```

constr/top.nxdc

```c
top=top

rst RST

ledr (LD15, LD14, LD13, LD12, LD11, LD10, LD9, LD8, LD7, LD6, LD5, LD4, LD3, LD2, LD1, LD0)
```
