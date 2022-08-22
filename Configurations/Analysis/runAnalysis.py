#!/usr/bin/env python
import optparse

import commonTools
import latinoTools
import combineTools
import analysisTools

if __name__ == '__main__':

    # Input parameters
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--action'        , dest='action'        , help='Action to be performed'        , default='shapes')
    parser.add_option('--configuration' , dest='configuration' , help='Configuration file'            , default='configuration.py')
    parser.add_option('--tag'           , dest='tag'           , help='Tag'                           , default='test')
    parser.add_option('--year'          , dest='year'          , help='year'                          , default='test')
    parser.add_option('--sigset'        , dest='sigset'        , help='Sample to run on'              , default='SM')
    parser.add_option('--fileset'       , dest='fileset'       , help='Input shape file'              , default='')
    parser.add_option('--option'        , dest='option'        , help='Options for the action'        , default='')
    parser.add_option('--keepallplots'  , dest='keepallplots'  , help='Keep all plots'                , default=False, action='store_true')
    parser.add_option('--shapedir'      , dest='shapedir'      , help='Directory to store shapes'     , default='./Shapes')
    parser.add_option('--plotsdir'      , dest='plotsdir'      , help='Directory to store plots'      , default='./Plots')
    parser.add_option('--cardsdir'      , dest='cardsdir'      , help='Directory to store datacards'  , default='./Datacards')
    parser.add_option('--datadir'       , dest='datadir'       , help='Directory wo store input data' , default='./Data')
    parser.add_option('--queue'         , dest='queue'         , help='Queue for the batch jobs'      , default='cms_high')
    parser.add_option('--logs'          , dest='logs'          , help='Directory with log files'      , default='./logs')
    (opt, args) = parser.parse_args()

    for tool in [ commonTools, latinoTools, combineTools, analysisTools ]:
        if hasattr(tool, opt.action):
            module = getattr(tool, opt.action)
            module(opt)

