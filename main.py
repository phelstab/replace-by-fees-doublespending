# ds.py
import argparse
import logging
import rbf

def main():
    parser = argparse.ArgumentParser(
            description="Attempt to double-spend a payment",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-t', action='store_true',
                        dest='testnet',
                        help='Enable testnet')
    parser.add_argument('-n', action='store_true',
                        dest='dryrun',
                        help="Dry-run; don't actually send the transactions")
    parser.add_argument('-d', action='store', type=int,
                        default=20,
                        dest='delay',
                        help="Delay in seconds between payment and double-spend")
    parser.add_argument('--dust', action='store', type=float,
                        default=0.0001,
                        help="Dust amount")
    parser.add_argument('--fee1', action='store', type=float,
                        metavar='FEEPERKB',
                        default=0.000014, # Miner's fee-per-KB for testnet
                        help='Fee-per-KB of payment transaction')
    parser.add_argument('--fee2', action='store', type=float,
                        metavar='FEEPERKB',
                        default=0.0014,
                        help='Fee-per-KB of double-spend transaction')

    parser.add_argument('--op-return', action='store_true',
                        help="Add OP_RETURN <data> output to payment tx")
    parser.add_argument('--multisig', action='store_true',
                        help="Add multisig output to payment tx")
    parser.add_argument('--optinrbf', action='store_true',
                        default=False,
                        help="Signal full-RBF opt-in (BIP125)")
    parser.add_argument('--bad-addr', action='append',
                        default=[],
                        help="Pay some dust to a 'bad' address to discourage propagation")

    parser.add_argument('address', action='store', type=str,
                        help='Address to double-spend')
    parser.add_argument('amount', action='store', type=float,
                        help='Amount to send')

    args = parser.parse_args()

    print("Arguments:")
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}") # Printing arguments for checking

    input("Press Enter to confirm and proceed...") # You need to press Enter to continue

    logging.root.setLevel('DEBUG')

    rpc = rbf.setup_rpc(args.testnet)
    rbf.create_transaction(rpc, args)

if __name__ == "__main__":
    main()