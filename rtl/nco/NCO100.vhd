library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nco100 is 
    generic(
        PHASE_WIDTH : integer := 32;
        ADDR_WIDTH  : integer := 6; -- 2^6 = 64 point
        OUT_WIDTH : integer := 16
    );
    port(
        clk : in std_logic;
        rst : in std_logic;
        phase_inc : in unsigned(PHASE_WIDTH-1 downto 0);
        sin_out : out signed(OUT_WIDTH - 1 downto 0);
        cos_out : out signed(OUT_WIDTH - 1 downto 0)
    );
end entity;

architecture ROM of nco100 is
    
    component nco_LUT  
    generic(
        ADDR_WIDTH  : integer := 6;
        OUT_WIDTH : integer := 16
    );
    port(
        clk : in std_logic;
        addr_sin : in unsigned(ADDR_WIDTH - 1 downto 0);
        addr_cos : in unsigned(ADDR_WIDTH - 1 downto 0);
        sin_abs : out signed(OUT_WIDTH - 1 downto 0);
        cos_abs : out signed(OUT_WIDTH - 1 downto 0)
    );
    end component;
    
    signal phase_acc_nco : unsigned (PHASE_WIDTH-1 downto 0):= (others => '0');
    signal addr_sin, addr_cos : unsigned (ADDR_WIDTH - 1 downto 0):= (others => '0');
    signal quadrant, quadrant_d : unsigned (1 downto 0):= (others => '0');
    signal sin_abs, cos_abs : signed (OUT_WIDTH - 1 downto 0):= (others => '0');
    signal sin_signed, cos_signed : signed(OUT_WIDTH -1 downto 0) := (others => '0'); 
    signal forward_addr : unsigned(ADDR_WIDTH - 1 downto 0);
    signal backward_addr : unsigned(ADDR_WIDTH - 1 downto 0);
begin

    -- extract quadrant (top 2 bits from phase_acc)
    quadrant <= phase_acc_nco(PHASE_WIDTH -1 downto PHASE_WIDTH -2);
    forward_addr <= phase_acc_nco(PHASE_WIDTH -3 downto PHASE_WIDTH-2-ADDR_WIDTH);
    backward_addr <= not phase_acc_nco(PHASE_WIDTH -3 downto PHASE_WIDTH-2-ADDR_WIDTH);

    PHASE_ACC: process (clk, rst)
    begin
        if rst = '1' then
            phase_acc_nco <= (others => '0');
        elsif  rising_edge(clk) then
            phase_acc_nco <= phase_acc_nco + phase_inc;
        end if; 
    end process;


    ASSIGN_ROM_ADDR: process(all)
    begin
        if quadrant(0) = '0' then       -- 1st / 3rd Quadrant 
            addr_sin <= forward_addr;
            addr_cos <= backward_addr;
        else
            addr_sin <= backward_addr;  -- 2nd / 4th Quadrant
            addr_cos <= forward_addr;
        end if;
    end process;

    READ_NCO_LUT: nco_LUT   -- 1 cycle latency
        generic map(
            ADDR_WIDTH  => ADDR_WIDTH,
            OUT_WIDTH => OUT_WIDTH
        )
        port map(
            clk => clk,
            addr_sin => addr_sin,
            addr_cos => addr_cos,
            sin_abs => sin_abs,
            cos_abs => cos_abs
        );

    SIGNED_SIN_COS : process(clk)
    begin
        if rising_edge(clk) then
            quadrant_d <= quadrant;  -- wait for 1 cycle delayed ROM data
            case quadrant_d is
            when "00" =>
                sin_signed <= sin_abs;
                cos_signed <= cos_abs;
            when "01" =>
                sin_signed <= sin_abs; 
                cos_signed <= not(cos_abs) + 1;
            when "10" =>
                sin_signed <= not(sin_abs) + 1; 
                cos_signed <= not(cos_abs) + 1;
            when "11" =>
                sin_signed <= not(sin_abs) + 1; 
                cos_signed <= cos_abs;
            when others =>
                sin_signed <= (others =>'0');
                cos_signed <= (others =>'0');
            end case;
        end if;
    end process;
    sin_out <= sin_signed;
    cos_out <= cos_signed;

end architecture;
