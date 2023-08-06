import sys, os
import argparse
import json
from json import JSONDecodeError

from hpogrid.components.defaults import *
from hpogrid.configuration import ConfigurationBase

class HPOConfiguration(ConfigurationBase):
    
    config_type = 'hpo'
    description = 'Manage configuration for hyperparameter optimization'
    usage = 'hpogrid hpo_config <action> <config_name> [<options>]'
    list_columns = ['HPO Configuration']
    show_columns = ['Attribute', 'Value']
    json_interpreted = ['stop', 'scheduler_param', 'algorithm_param', 'resource']
    
    @staticmethod
    def get_parser_test():
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('name', help= "Name given to the configuration file")
        parent_parser.add_argument('-a','--algorithm', metavar='',
                            help='Algorithm for hyperparameter optimization. '+\
                                 'Allowed values: {}'.format(','.join(kSearchAlgorithms)), 
                            default=kDefaultSearchAlgorithm, choices=kSearchAlgorithms)
        parent_parser.add_argument('-m', '--metric', metavar='',
                            help='Evaluation metric to be optimized',
                            required=True)
        parent_parser.add_argument('-e', '--extra_metrics', metavar='', nargs='+',
                            help='Additional metrics to be saved during the training',
                            required=False)
        parent_parser.add_argument('-o', '--mode', metavar='', 
                            help='Mode of optimization (either "min" or "max")', 
                            choices=kMetricMode,
                            required=True)
        parent_parser.add_argument('-s','--scheduler', metavar='',
                            help='Trial scheduling method for hyperparameter optimization. '+\
                                 'Allowed values: {}'.format(','.join(kSchedulers)),
                            default=kDefaultScheduler, choices=kSchedulers)
        parent_parser.add_argument('-n','--num_trials', metavar='',
                            help='Number of trials (search points)', 
                            type=int, required=True)
        parent_parser.add_argument('-c','--max_concurrent', metavar='',
                            help='Maximum number of trials to be run concurrently', 
                            type=int, default=kDefaultMaxConcurrent)            
        parent_parser.add_argument('-l', '--log_dir', metavar='',
                            help='Logging directory',
                            default=kDefaultLogDir)
        parent_parser.add_argument('-v','--verbose', metavar='', type=int, 
                            default=kDefaultVerbosity,
                            help='Verbosity level of Ray Tune')
        parent_parser.add_argument('--stop', metavar='',
                            help='Stopping criteria for the training',
                            default=kDefaultStopping)
        parent_parser.add_argument('-r','--resource', metavar='',
                            help='Resource allocated to each trial',
                            default=kDefaultResource)            
        parent_parser.add_argument('--scheduler_param', metavar='',
                            help='Extra parameters given to the trial scheduler', 
                            default=kDefaultSchedulerParam)
        parent_parser.add_argument('--algorithm_param', metavar='',
                            help='Extra parameters given to the hyperparameter optimization algorithm',
                            default=kDefaultAlgorithmParam)
        parser = ConfigurationBase.get_parser_test('hpo_config',
            parent_parser=parent_parser,
            description='Manage configuration for hyperparameter optimization',
            usage='hpogrid hpo_config <action> <config_name> [<options>]')
        return parser
            
    
    def get_parser(self, action=None):
        parser = self.get_base_parser()        
        if action in kConfigAction:
            parser.add_argument('name', help= "Name given to the configuration file")
            parser.add_argument('-a','--algorithm', 
                                help='Algorithm for hyperparameter optimization', 
                                default=kDefaultSearchAlgorithm, choices=kSearchAlgorithms)
            parser.add_argument('-m', '--metric', metavar='',
                                help='Evaluation metric to be optimized',
                                required=True)
            parser.add_argument('-e', '--extra_metrics', metavar='', nargs='+',
                                help='Additional metrics to be saved during the training',
                                required=False)
            parser.add_argument('-o', '--mode', 
                                help='Mode of optimization (either "min" or "max")', 
                                choices=kMetricMode,
                                required=True)
            parser.add_argument('-s','--scheduler', 
                                help='Trial scheduling method for hyperparameter optimization',
                                default=kDefaultScheduler, choices=kSchedulers)
            parser.add_argument('-n','--num_trials', metavar='',
                                help='Number of trials (search points)', 
                                type=int, required=True)
            parser.add_argument('-c','--max_concurrent', metavar='',
                                help='Maximum number of trials to be run concurrently', 
                                type=int, default=kDefaultMaxConcurrent)            
            parser.add_argument('-l', '--log_dir', metavar='',
                                help='Logging directory',
                                default=kDefaultLogDir)
            parser.add_argument('-v','--verbose', metavar='', type=int, 
                                default=kDefaultVerbosity,
                                help='Verbosity level of Ray Tune')
            parser.add_argument('--stop', metavar='',
                                help='Stopping criteria for the training',
                                default=kDefaultStopping)
            parser.add_argument('-r','--resource', metavar='',
                                help='Resource allocated to each trial',
                                default=kDefaultResource)            
            parser.add_argument('--scheduler_param', metavar='',
                                help='Extra parameters given to the trial scheduler', 
                                default=kDefaultSchedulerParam)
            parser.add_argument('--algorithm_param', metavar='',
                                help='Extra parameters given to the hyperparameter optimization algorithm',
                                default=kDefaultAlgorithmParam)
        else:
            parser = super().get_parser(action)
        return parser