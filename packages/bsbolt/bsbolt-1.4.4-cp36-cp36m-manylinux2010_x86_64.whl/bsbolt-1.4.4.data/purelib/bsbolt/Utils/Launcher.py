import datetime
import os
import time
from bsbolt.Align.AlignReads import BisulfiteAlignmentAndProcessing
from bsbolt.CallMethylation.ProcessMethylationContigs import ProcessContigs
from bsbolt.Impute.kNN_Impute import ImputeMissingValues
from bsbolt.Index.RRBSIndex import RRBSBuild
from bsbolt.Index.WholeGenomeIndex import WholeGenomeBuild
from bsbolt.Matrix.MatrixAggregator import AggregateMatrix
from bsbolt.Simulate import SimulateMethylatedReads
from bsbolt.Utils.UtilityFunctions import index_bam, get_external_paths, sort_bam

bwa_path, wgsim_path, stream_bam = get_external_paths()


def launch_index(arguments):
    if arguments.rrbs:
        print(f'Generating RRBS Database at {arguments.DB}: '
              f'lower bound {arguments.rrbs_lower}, upper bound {arguments.rrbs_upper}: '
              f'Cut Format {arguments.rrbs_cut_format}')
        index = RRBSBuild(reference_file=arguments.G,
                          genome_database=arguments.DB,
                          cut_format=arguments.rrbs_cut_format,
                          lower_bound=arguments.rrbs_lower,
                          upper_bound=arguments.rrbs_upper,
                          block_size=arguments.B,
                          ignore_alt=arguments.IA)
        index.generate_rrbs_database()
    else:
        print(f'Generating WGBS Database at {arguments.DB}')
        index = WholeGenomeBuild(reference_file=arguments.G,
                                 genome_database=arguments.DB,
                                 mappable_regions=arguments.MR,
                                 block_size=arguments.B,
                                 ignore_alt=arguments.IA)
        index.generate_bsb_database()


def align_bisulfite(bwa_cmd, output_path, output_threads):
    start = time.time()
    print(' '.join(bwa_cmd))
    bs_alignment = BisulfiteAlignmentAndProcessing(bwa_cmd, output_path, output_threads)
    bs_alignment.align_reads()
    alignment_time = datetime.timedelta(seconds=round(time.time() - start))
    print(f'Alignment Complete: Time {alignment_time}')
    print('------------------------------')
    mapping_stats = process_mapping_statistics(bs_alignment.mapping_statistics)
    print(mapping_stats)


def process_mapping_statistics(mapping_dict):
    dict(TotalReads=0, TotalAlignments=0, BSAmbiguous=0, C_C2T=0, C_G2A=0,
         W_C2T=0, W_G2A=0, Unaligned=0)
    processed_list = []
    try:
        mappability = (mapping_dict['TotalAlignments'] - mapping_dict['Unaligned']) / mapping_dict['TotalAlignments']
    except ZeroDivisionError:
        mappability = '0.000%'
    processed_list.append(f'Total Reads: {mapping_dict["TotalReads"]}')
    processed_list.append(f'Mappability: {mappability * 100:.3f} %')
    processed_list.append('------------------------------')
    processed_list.append(f'Reads Mapped to Watson_C2T: {mapping_dict["W_C2T"]}')
    processed_list.append(f'Reads Mapped to Crick_C2T: {mapping_dict["C_C2T"]}')
    processed_list.append(f'Reads Mapped to Watson_G2A: {mapping_dict["W_G2A"]}')
    processed_list.append(f'Reads Mapped to Crick_G2A: {mapping_dict["C_G2A"]}')
    processed_list.append('------------------------------')
    processed_list.append(f'Unmapped Reads (Single / Paired Ends): {mapping_dict["Unaligned"]}')
    processed_list.append(f'Bisulfite Ambiguous: {mapping_dict["BSAmbiguous"]}')
    return '\n'.join(processed_list)


def launch_alignment(arguments):
    bsb_command_dict = {arg[0]: str(arg[1]) for arg in arguments._get_kwargs()}
    bwa_cmd = [bwa_path, 'mem', '-Y']
    if bsb_command_dict['UN'] == 'True':
        bwa_cmd.extend(['-z'])
    bool_args = ['M', 'S', 'j', 'p']
    for arg in bool_args:
        if bsb_command_dict[arg] == 'True':
            bwa_cmd.append(f'-{arg}')
    default_args = ['A', 'B', 'D', 'E', 'L', 'T', 'U', 'W', 'c', 'd', 'k', 'm', 'r', 't', 'w', 'y']
    for arg in default_args:
        bwa_cmd.extend([f'-{arg}', bsb_command_dict[arg]])
    if bsb_command_dict['H'] != 'None':
        bwa_cmd.extend(['-H', bsb_command_dict['H']])
    if bsb_command_dict['I'] != 'None':
        bwa_cmd.extend(['-I', bsb_command_dict['I']])
    if bsb_command_dict['INDEL']:
        bwa_cmd.extend(['-O', bsb_command_dict['INDEL']])
    if bsb_command_dict['XA']:
        bwa_cmd.extend(['-h', bsb_command_dict['XA']])
    bwa_cmd.extend(['-e', bsb_command_dict['SP']])
    bwa_cmd.extend(['-l', bsb_command_dict['CP']])
    bwa_cmd.extend(['-n', bsb_command_dict['CT']])
    bwa_cmd.extend(['-Z', bsb_command_dict['DR']])
    database = bsb_command_dict['DB']
    if not database.endswith('.fa'):
        if not database.endswith('/'):
            database = f'{database}/BSB_ref.fa'
        else:
            database = f'{database}BSB_ref.fa'
        assert os.path.exists(database), f'-DB {arguments.DB} does not exist, please index genome'
        assert os.path.exists(f'{database}.opac'), f'-DB {arguments.DB} not complete, please re-index genome'
    bwa_cmd.append(database)
    bwa_cmd.append(bsb_command_dict['F1'])
    assert os.path.exists(arguments.F1), f'-F1 {arguments.F1} does not exist, please check path'
    if bsb_command_dict['F2'] != 'None':
        bwa_cmd.append(bsb_command_dict['F2'])
        assert os.path.exists(arguments.F2), f'-F2 {arguments.F2} does not exist, please check path'
    align_bisulfite(bwa_cmd, arguments.O, arguments.OT)


def launch_sort_bam(arguments):
    sort_bam(bam_output=arguments.O, bam_input=arguments.I)


def launch_index_bam(arguments):
    index_bam(bam_input=arguments.I)


def launch_methylation_call(arguments):
    if arguments.CG and arguments.ATCG:
        assert False, 'Reporting only CG sites notes compatible with .ATCGmap output'
    methylation_call = ProcessContigs(input_file=arguments.I,
                                      genome_database=arguments.DB,
                                      output_prefix=arguments.O,
                                      remove_ccgg=arguments.remove_ccgg,
                                      text_output=arguments.text,
                                      min_read_depth=arguments.min,
                                      threads=arguments.t,
                                      verbose=arguments.verbose,
                                      min_base_quality=arguments.BQ,
                                      min_mapping_quality=arguments.MQ,
                                      cg_only=arguments.CG,
                                      ATCGmap=arguments.ATCG,
                                      ignore_orphans=arguments.IO,
                                      bedgraph_output=arguments.BG)
    methylation_call.process_contigs()
    methylation_call.watch_pool()


def launch_matrix_aggregation(arguments):
    def get_sample_info(file_path):
        file_list = []
        with open(file_path, 'r') as file:
            for line in file:
                file_list.append(line.replace('\n', ''))
        return file_list

    if len(arguments.F) == 1:
        arguments.F = get_sample_info(arguments.F[0])
    if arguments.S:
        if len(arguments.S) == 1:
            arguments.S = get_sample_info(arguments.S[0])

    matrix = AggregateMatrix(file_list=arguments.F,
                             sample_list=arguments.S,
                             min_site_coverage=arguments.min_coverage,
                             site_proportion_threshold=arguments.min_sample,
                             output_path=arguments.O,
                             cg_only=arguments.CG,
                             verbose=arguments.verbose,
                             threads=arguments.t,
                             count_matrix=arguments.count)
    matrix.aggregate_matrix()


def launch_simulation(arguments):
    read_simulation = SimulateMethylatedReads(reference_file=arguments.G,
                                              sim_output=arguments.O,
                                              sequencing_error=arguments.SE, mutation_rate=arguments.MR,
                                              mutation_indel_fraction=arguments.MI,
                                              indel_extension_probability=arguments.ME, random_seed=arguments.RS,
                                              paired_end=arguments.PE, read_length=arguments.RL,
                                              read_depth=arguments.RD, undirectional=arguments.U,
                                              methylation_reference=arguments.BR,
                                              cgmap=arguments.CG, ambiguous_base_cutoff=arguments.NF,
                                              haplotype_mode=arguments.HA,
                                              pe_fragment_size=arguments.FM, insert_deviation=arguments.SM,
                                              mean_insert_size=arguments.IM,
                                              collect_ch_sites=arguments.CH, collect_sim_stats=arguments.NS,
                                              verbose=arguments.verbose,
                                              overwrite_db=arguments.overwrite)

    read_simulation.run_simulation()


def launch_imputation(arguments):
    output_path = arguments.O
    if not output_path:
        output_path = f'{arguments.M}_imputed.txt'
    impute = ImputeMissingValues(input_matrix_file=arguments.M, batch_size=arguments.B,
                                 imputation_window_size=arguments.W, k=arguments.k, threads=arguments.t,
                                 verbose=arguments.verbose, output_path=output_path, randomize_batch=arguments.R)
    impute.import_matrix()
    impute.impute_values()
    impute.output_imputed_matrix()


bsb_launch = {'Index': launch_index,
              'Align': launch_alignment,
              'CallMethylation': launch_methylation_call,
              'AggregateMatrix': launch_matrix_aggregation,
              'Simulate': launch_simulation,
              'Impute': launch_imputation,
              'Sort': launch_sort_bam,
              'BamIndex': launch_index_bam}
