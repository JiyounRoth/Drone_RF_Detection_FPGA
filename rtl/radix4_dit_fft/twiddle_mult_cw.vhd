
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;


entity twiddle_mult_cw is
    generic (
        D_WIDTH : natural := 16;
        A_WIDTH : natural := 32
    );
    Port (
        clk     : in std_logic;
        en      : in std_logic;
        c   : in signed(D_WIDTH - 1 downto 0);
        s   : in signed(D_WIDTH - 1 downto 0);
        re1   : in signed(D_WIDTH - 1 downto 0);
        im1   : in signed(D_WIDTH - 1 downto 0);
        re2   : in signed(D_WIDTH - 1 downto 0);
        im2   : in signed(D_WIDTH - 1 downto 0);
        r_out   : out signed(D_WIDTH - 1 downto 0);
        i_out   : out signed(D_WIDTH - 1 downto 0)
     );
end twiddle_mult_cw;

architecture arch_dsp48_optimized of twiddle_mult_cw is
    function sticky_bit_scan(vec: std_logic_vector(A_WIDTH - D_WIDTH - 3 downto 0)) return std_logic is
        variable sb : std_logic := '0';
    begin
        for i in vec'range loop
            sb := sb or vec(i);    
        end loop;
        return sb;
    end function;
    
    function round_to_even(num : signed(A_WIDTH - 1 downto 0)) return signed is
        variable gb,rb,sb : std_logic := '0';
        variable num_truncated: signed(D_WIDTH - 1 downto 0); 
        variable num_rounded : signed(D_WIDTH - 1 downto 0);
    begin
        gb :=  num(A_WIDTH - D_WIDTH - 1);
        rb :=  num(A_WIDTH - D_WIDTH - 2);
        sb :=  sticky_bit_scan(std_logic_vector(num(A_WIDTH - D_WIDTH - 3 downto 0))); 
        num_truncated := num(A_WIDTH - 1 downto A_WIDTH - D_WIDTH);
        if gb = '1' then
            if rb = '1' or sb = '1' then  -- remains > 0.5
                num_rounded := num_truncated + 1; 
            else
                if num_truncated(0) = '1' then
                    num_rounded := num_truncated + 1;
                else
                    num_rounded := num_truncated;
                end if;
            end if;
        else
            num_rounded := num_truncated;
        end if;   
        return num_rounded;
    end function;
    signal x, x_s1, x_s2     : signed(D_WIDTH - 1 downto 0);
    signal y, y_s1, y_s2     : signed(D_WIDTH - 1 downto 0);
    signal c_s1, c_s2        : signed(D_WIDTH - 1 downto 0);
    signal s_s1, s_s2        : signed(D_WIDTH - 1 downto 0);
    signal x_minus_y  : signed(D_WIDTH - 1 downto 0);
    signal c_minus_s  : signed(D_WIDTH - 1 downto 0);
    signal c_plus_s    : signed(D_WIDTH - 1 downto 0);
    signal c_minus_s_mult_y         : signed(A_WIDTH - 1 downto 0);
    signal c_plus_s_mult_x          : signed(A_WIDTH - 1 downto 0);
    signal z, z_s1                  : signed(A_WIDTH - 1 downto 0);
    signal r, i                     : signed(A_WIDTH - 1 downto 0);
    signal r_rd_even, i_rd_even      : signed(D_WIDTH - 1 downto 0);
begin

    STATE1: process(clk)
    begin
        if rising_edge(clk) then
            if en = '1' then
                x       <= re2 + im1;        --  x= (a2 + b1)
                y       <= im2 - re1;        --  y= j(b2 - a1)
                c_s1    <= c;
                s_s1    <= s;
            end if;
        end if;
    end process;
   
    STATE2: process(clk)
    begin
        if rising_edge(clk) then
            if en = '1' then
                 x_minus_y  <= x - y;          -- (X-Y)
                 x_s1       <= x;
                 y_s1       <= y;
                 c_s2       <= c_s1;
                 s_s2       <= s_s1;
            end if;
        end if;
    end process;
   
    STATE3: process(clk)
    begin
        if rising_edge(clk) then
            if en = '1' then
                z         <= c_s2 * x_minus_y; -- Z = C(X-Y) 
                x_s2      <= x_s1;
                y_s2      <= y_s1;
                c_minus_s <= c_s2 - s_s2;    -- (c-s)
                c_plus_s  <= c_s2 + s_s2;    -- (c+s)
            end if;
        end if;
    end process;
   
    STATE4: process(clk)
    begin
        if rising_edge(clk) then
            if en = '1' then
                z_s1 <= z ;
                c_minus_s_mult_y <= c_minus_s * y_s2;  -- (C-S)Y
                c_plus_s_mult_x  <= c_plus_s * x_s2;   -- (C+S)X
            end if;
        end if;
    end process;
    
    STATE5: process(clk)
    begin
        if rising_edge(clk) then
            if en = '1' then        
                r <= c_minus_s_mult_y + z_s1;  
                i <= c_plus_s_mult_x - z_s1;
            end if;
        end if;
    end process;
    
    STATE6_rounding: process(clk)
    begin
        if rising_edge(clk) then
            if en = '1' then
                r_rd_even <= round_to_even(r);
                i_rd_even <= round_to_even(i);        
            end if;
        end if;
    end process;
    r_out <= r_rd_even;
    i_out <= i_rd_even;
  
end arch_dsp48_optimized;
