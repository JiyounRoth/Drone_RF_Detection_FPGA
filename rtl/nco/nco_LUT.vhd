-- sin_lut stores quater-wave absolute amplitude values (0°~90°)
-- sin_abs, cos_abs outputs are absolute values only
-- sign and address folding is handled in upper NCO logic


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nco_LUT is
    generic(
        ADDR_WIDTH  : integer := 6;
        OUT_WIDTH : integer := 16
    );
    port (
        clk : in std_logic;
        en  : in std_logic;
        addr_sin : in unsigned(ADDR_WIDTH - 1 downto 0);
        addr_cos : in unsigned(ADDR_WIDTH - 1 downto 0);
        sin_abs : out signed(OUT_WIDTH - 1 downto 0);
        cos_abs : out signed(OUT_WIDTH - 1 downto 0)
    );
end entity;

architecture ROM of nco_LUT is
    type lut_type is array (0 to 2**(ADDR_WIDTH)-1) of signed(OUT_WIDTH - 1 downto 0);
    constant sin_lut : lut_type := (
         0 => signed'("0000000000000000"),
         1 => signed'("0000001100110000"),
         2 => signed'("0000011001100001"),
         3 => signed'("0000100110010000"),
         4 => signed'("0000110010111110"),
         5 => signed'("0000111111101010"),
         6 => signed'("0001001100010011"),
         7 => signed'("0001011000111001"),
         8 => signed'("0001100101011100"),
         9 => signed'("0001110001111011"),
        10 => signed'("0001111110010101"),
        11 => signed'("0010001010101010"),
        12 => signed'("0010010110111010"),
        13 => signed'("0010100011000011"),
        14 => signed'("0010101111000110"),
        15 => signed'("0010111011000011"),
        16 => signed'("0011000110110111"),
        17 => signed'("0011010010100100"),
        18 => signed'("0011011110001001"),
        19 => signed'("0011101001100100"),
        20 => signed'("0011110100110110"),
        21 => signed'("0011111111111111"),
        22 => signed'("0100001010111101"),
        23 => signed'("0100010101110001"),
        24 => signed'("0100100000011010"),
        25 => signed'("0100101010110111"),
        26 => signed'("0100110101001000"),
        27 => signed'("0100111111001101"),
        28 => signed'("0101001001000110"),
        29 => signed'("0101010010110001"),
        30 => signed'("0101011100001111"),
        31 => signed'("0101100101011111"),
        32 => signed'("0101101110100000"),
        33 => signed'("0101110111010011"),
        34 => signed'("0101111111111000"),
        35 => signed'("0110001000001100"),
        36 => signed'("0110010000010010"),
        37 => signed'("0110011000000111"),
        38 => signed'("0110011111101100"),
        39 => signed'("0110100111000001"),
        40 => signed'("0110101110000101"),
        41 => signed'("0110110100110111"),
        42 => signed'("0110111011011001"),
        43 => signed'("0111000001101000"),
        44 => signed'("0111000111100110"),
        45 => signed'("0111001101010010"),
        46 => signed'("0111010010101011"),
        47 => signed'("0111010111110010"),
        48 => signed'("0111011100100101"),
        49 => signed'("0111100001000110"),
        50 => signed'("0111100101010100"),
        51 => signed'("0111101001001111"),
        52 => signed'("0111101100110110"),
        53 => signed'("0111110000001001"),
        54 => signed'("0111110011001001"),
        55 => signed'("0111110101110101"),
        56 => signed'("0111111000001101"),
        57 => signed'("0111111010010001"),
        58 => signed'("0111111100000000"),
        59 => signed'("0111111101011100"),
        60 => signed'("0111111110100011"),
        61 => signed'("0111111111010110"),
        62 => signed'("0111111111110100"),
        63 => signed'("0111111111111111")
    );
    
begin

process(clk)
begin
    if rising_edge(clk) then
        if en = '1' then
            sin_abs <= sin_lut(to_integer(addr_sin));
            cos_abs <= sin_lut(to_integer(addr_cos));
        end if;
    end if;
end process;

end architecture;
