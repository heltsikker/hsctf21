import angr

p = angr.Project("./management")

initial_state = p.factory.full_init_state()

sim_mgr = p.factory.simulation_manager(initial_state)

sim_mgr.explore(find=0x402516)

for state in sim_mgr.found:
    flag = state.posix.dumps(0)
    print("Potential flag: " + flag.decode())
