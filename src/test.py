import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

valid_digits = [0b0000110, 0b1011011, 0b1001111, 0b1100110, 0b1101101, 0b1111100]

@cocotb.test()
async def test_diceroll(dut):
		dut._log.info("start")
		dut.ROLL.value = 0
		clock = Clock(dut.CLK, 0.2, units="ms")
		cocotb.start_soon(clock.start())
		
		dut._log.info("reset")
		dut.RST.value = 1
		await ClockCycles(dut.CLK, 5)
		dut.RST.value = 0
		await ClockCycles(dut.CLK, 20)
		assert dut.LEDS.value == 0b10000110
		
		for j in range(0, 8):
			dut._log.info(f'Roll {j + 1}')
			dut.ROLL.value = 1
			last_val = dut.LEDS.value
			assert (last_val & 0b01111111) in valid_digits
			await ClockCycles(dut.CLK, random.randint(3, 128))
			assert dut.LEDS.value == last_val & 0b01111111
			dut.ROLL.value = 0
			await ClockCycles(dut.CLK, 2)
			
			# Testing randomness is unfortunately a bit hard
			clock_cycles = 3
			last_val = dut.LEDS.value
			assert last_val in valid_digits
			counter = 0
			for i in range(0, 157):
				await ClockCycles(dut.CLK, clock_cycles - 1)
				assert dut.LEDS.value == last_val
				# Can’t just check the value is different. It is likely for the RNG to produce the same number twice
				await ClockCycles(dut.CLK, 1)
				if dut.LEDS.value == last_val: # Fail if the display shows the same number 7 times in a row (statistically unlikely)
					counter += 1
					assert counter < 7
				else:
					counter = 0
				last_val = dut.LEDS.value
				assert last_val in valid_digits
				clock_cycles += 1
			await ClockCycles(dut.CLK, clock_cycles)
			last_val = dut.LEDS.value
			assert (last_val & (1 << 7)) != 0
			await ClockCycles(dut.CLK, clock_cycles * 3)
			assert dut.LEDS.value == last_val
			assert (last_val & 0b01111111) in valid_digits
