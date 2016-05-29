require "initenv"

function create_network(args)


    local net = nn.Sequential()
    local hidnum = 128
    ---[[
    local input_dim = args.state_dim
    
    net:add(nn.Reshape(input_dim*args.hist_len))
    net:add(nn.Linear(args.hist_len*input_dim,hidnum))
    net:add(args.nl())
    net:add(nn.Linear(hidnum, hidnum))
    net:add(args.nl())
    net:add(nn.Linear(hidnum, args.n_actions))
    --]]
    if args.gpu >=0 then
        net:cuda()
    end

    if args.verbose >= 2 then
        print(net)
    end
	

    return net
end

return function(args)
    args.nl  = nn.Rectifier
    return create_network(args)
end


